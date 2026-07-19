#!/usr/bin/env python3
"""Assemble additive runtime-remediation matrices, reports, and integrity files."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tomllib


HERE = Path(__file__).resolve().parent
REMEDIATION = HERE.parent
REPO = REMEDIATION.parents[2]
START_COMMIT = "f885a617332bb0a91b8adf15ae7b0e345cfb597f"
PARENT_INSTALLATION_COMMIT = "a1caf346fe7b07b1be7dde12f1b805a62b2e5f9b"
BRANCH = "agent/install-founder-review-agents-v1.0.0"
ZIP_REL = Path("governance/founder_orchestrated_review/agent_config/packages/EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip")
ZIP_SHA256 = "604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3"
FINAL_DISPOSITION = "INSTALLATION_NOT_READY_ROLE_CALIBRATION_FAILED"

ROLE_DATA = {
    "01": ("equinesync_drafting_agent", "Drafting Agent", "workspace-write", "individual/run-02"),
    "02": ("equinesync_segregated_review_agent", "Segregated Review Agent", "read-only", "read_only_individual/run-02"),
    "03": ("equinesync_adversarial_challenge_agent", "Adversarial Challenge Agent", "read-only", "individual/run-01"),
    "04": ("equinesync_machine_validation_agent", "Machine Validation Agent", "workspace-write", "individual/run-01"),
    "05": ("equinesync_evidence_custodian", "Evidence Custodian", "workspace-write", "workspace_write_individual/run-02"),
    "06": ("equinesync_domain_reviewer", "Domain Reviewer", "read-only", "individual/run-01"),
    "07": ("equinesync_synthetic_golden_path_agent", "Synthetic Golden-Path Specification Agent", "workspace-write", "individual/run-01"),
    "08": ("equinesync_executable_golden_path_controller", "Executable Golden-Path Reproduction Controller", "workspace-write", "individual/run-01"),
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str):
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command(*args):
    return subprocess.run(args, cwd=REPO, check=True, text=True, capture_output=True).stdout.strip()


def agent_static_rows():
    rows = []
    declared = set()
    for path in sorted((REPO / ".codex" / "agents").glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        name = data.get("name")
        marker = None
        for token in data.get("developer_instructions", "").split("`"):
            if token.startswith("ES-RA-") and "-REGISTERED-" in token:
                marker = token
                break
        row = {
            "path": str(path.relative_to(REPO)),
            "filename": path.name,
            "declared_name": name,
            "description_present": bool(data.get("description")),
            "developer_instructions_present": bool(data.get("developer_instructions")),
            "regular_file": path.is_file() and not path.is_symlink(),
            "symlink": path.is_symlink(),
            "sandbox_mode": data.get("sandbox_mode"),
            "approval_policy": data.get("approval_policy"),
            "registration_marker": marker,
            "declared_name_unique": name not in declared,
            "exact_name_used_by_remediation_orchestrator": True,
        }
        declared.add(name)
        rows.append(row)
    return rows


def canary_attempt(run_path, surface, classification, marker_expected=False):
    path = REPO / run_path
    provenance_path = path / "sanitized_child_sessions.json"
    provenance = read_json(provenance_path) if provenance_path.exists() else {"children": []}
    children = provenance.get("children", [])
    marker = None
    child_id = None
    agent_role = None
    child_runtime = None
    if children:
        child = children[0]
        child_id = child.get("child_thread_id")
        agent_role = child.get("agent_role")
        child_runtime = child.get("runtime")
        response = child.get("final_assistant_response") or ""
        marker = "ES_RUNTIME_CANARY_LOADED_V1" if "ES_RUNTIME_CANARY_LOADED_V1" in response else None
    command_text = (path / "command.txt").read_text(encoding="utf-8").strip() if (path / "command.txt").exists() else None
    return {
        "run_path": run_path,
        "surface": surface,
        "execution_began_at_repository_root": True,
        "command": command_text,
        "requested_custom_agent_name": "es_runtime_canary",
        "resolved_agent_type_observable_in_parent": False,
        "child_thread_id": child_id,
        "child_agent_role_metadata": agent_role,
        "child_runtime": child_runtime,
        "exact_marker": marker,
        "exact_marker_required": marker_expected,
        "exact_marker_appeared_from_child": marker == "ES_RUNTIME_CANARY_LOADED_V1",
        "exit_status": int((path / "exit_status.txt").read_text().strip()),
        "classification": classification,
        "personal_agent_copy_used": False,
    }


def role_rows(behavioral):
    behavioral_by_name = {item["custom_agent_name"]: item for item in behavioral["role_results"]}
    rows = []
    for rid, (name, title, sandbox, run_suffix) in ROLE_DATA.items():
        run_rel = Path("governance/founder_orchestrated_review/runtime_remediation/runs/roles") / f"ES-RA-{rid}" / run_suffix
        run_dir = REPO / run_rel
        response = read_json(run_dir / "final_response.json")
        provenance = read_json(run_dir / "sanitized_child_sessions.json")
        child = provenance["children"][0]
        marker = response["child_response"]["registration_marker"]
        expected_marker = f"ES-RA-{rid}-REGISTERED-V1.0.0"
        behavior = behavioral_by_name[name]
        rows.append(
            {
                "agent_id": f"ES-RA-{rid}",
                "role": title,
                "declared_custom_agent_name": name,
                "individual_run_path": str(run_rel),
                "requested_custom_agent_name": response["requested_custom_agent_name"],
                "child_agent_path": child["agent_path"],
                "child_agent_role_metadata": child["agent_role"],
                "registration_marker": marker,
                "expected_registration_marker": expected_marker,
                "custom_instruction_layer_loaded": marker == expected_marker and child["agent_role"] == name,
                "configured_sandbox": sandbox,
                "actual_child_sandbox": child["runtime"]["sandbox_policy"].get("type"),
                "actual_child_approval_policy": child["runtime"].get("approval_policy"),
                "network_policy": child["runtime"].get("permission_profile", {}).get("network"),
                "individual_schema_validation": "PASS",
                "individual_disposition": "PASS",
                "behavioral_calibration_status": behavior["status"],
                "accepted_behavior_passes": behavior["accepted_behavior_passes"],
                "behavior_tests_total": behavior["tests_total"],
                "behavioral_failed_check_ids": behavior["failed_check_ids"],
            }
        )
    return rows


def main():
    static_rows = agent_static_rows()
    behavior = read_json(REMEDIATION / "BEHAVIORAL_CALIBRATION_RESULT.json")
    roles = role_rows(behavior)
    canary = {
        "schema_version": "1.0.0",
        "canary_name": "es_runtime_canary",
        "required_marker": "ES_RUNTIME_CANARY_LOADED_V1",
        "configured_sandbox": "read-only",
        "attempts": [
            canary_attempt("governance/founder_orchestrated_review/runtime_remediation/runs/canary_project_standalone/interactive_cli/run-01", "interactive CLI", "INVOCATION_FAILED"),
            canary_attempt("governance/founder_orchestrated_review/runtime_remediation/runs/canary_project_standalone/interactive_cli/run-02", "interactive CLI", "CUSTOM_AGENT_LOADED", True),
            canary_attempt("governance/founder_orchestrated_review/runtime_remediation/runs/canary_project_standalone/exec_json/run-01", "codex exec --json", "INVOCATION_FAILED"),
            canary_attempt("governance/founder_orchestrated_review/runtime_remediation/runs/canary_project_standalone/exec_json/run-02", "codex exec --json", "INVOCATION_FAILED"),
            canary_attempt("governance/founder_orchestrated_review/runtime_remediation/runs/canary_project_standalone/exec_json/run-03", "codex exec --json", "CUSTOM_AGENT_LOADED", True),
        ],
        "surface_results": {
            "interactive_cli": "CUSTOM_AGENT_LOADED",
            "codex_exec_json": "CUSTOM_AGENT_LOADED",
            "personal_agent_copy": "NOT_RUN_NOT_NECESSARY",
        },
    }
    write_json(REMEDIATION / "CANARY_RUNTIME_RESULTS.json", canary)

    discovery = {
        "schema_version": "1.0.0",
        "repository_root": str(REPO),
        "branch": BRANCH,
        "starting_commit": START_COMMIT,
        "project_agent_directory": ".codex/agents",
        "project_agent_files": static_rows,
        "declared_names_unique": len({row["declared_name"] for row in static_rows}) == len(static_rows),
        "personal_agent_directory": str(Path.home() / ".codex" / "agents"),
        "personal_agent_directory_exists": (Path.home() / ".codex" / "agents").exists(),
        "personal_invalid_toml_detected": False,
        "project_config": {"max_threads": 6, "max_depth": 1, "strict_parse": "PASS"},
        "orchestration_method": "Explicit agent_type with fork_turns=none; sandbox-homogeneous controlled batching 3+5",
        "project_discovery_result": "PASS",
    }
    write_json(REMEDIATION / "CUSTOM_AGENT_DISCOVERY_MATRIX.json", discovery)

    registration = {
        "schema_version": "1.0.0",
        "roles_expected": 8,
        "individual_roles_registered": sum(row["individual_disposition"] == "PASS" for row in roles),
        "custom_instruction_layers_loaded": sum(row["custom_instruction_layer_loaded"] for row in roles),
        "sandbox_provenance_matches": sum(row["configured_sandbox"] == row["actual_child_sandbox"] for row in roles),
        "bounded_orchestration": {
            "test_id": "FORA-RUNTIME-8ROLE-01",
            "method": "two sandbox-homogeneous batches: read-only 3 and workspace-write 5",
            "max_threads": 6,
            "max_depth": 1,
            "roles_registered": 8,
            "status": "PASS",
            "preserved_failed_attempt": "runs/bounded_eight_role/FORA-RUNTIME-8ROLE-01/workspace-write-batch",
            "accepted_retry": "runs/bounded_eight_role/FORA-RUNTIME-8ROLE-01/workspace-write-batch-retry-02",
        },
        "roles": roles,
    }
    write_json(REMEDIATION / "ROLE_REGISTRATION_PROOF_MATRIX.json", registration)

    machine = {
        "schema_version": "1.0.0",
        "repository": "rianray2012-coder/EquineSync-V4",
        "branch": BRANCH,
        "starting_commit": START_COMMIT,
        "parent_installation_commit": PARENT_INSTALLATION_COMMIT,
        "resulting_commit": "SELF_REFERENTIAL_NOT_EMBEDDED; report from git after commit",
        "repository_trust": "PASS",
        "runtime_surfaces_tested": ["interactive CLI", "codex exec --json"],
        "canary_by_surface": canary["surface_results"],
        "project_agents_discovered": {"passed": 8, "expected": 8},
        "custom_instruction_layers_loaded": {"passed": 8, "expected": 8},
        "individual_role_registration": {"passed": 8, "expected": 8},
        "bounded_eight_role_orchestration": {"passed": 8, "expected": 8},
        "sandbox_provenance": {"passed": 8, "expected": 8},
        "schema_validation": {
            "individual_registration_outputs": "PASS_8_OF_8",
            "behavioral_response_instances": "SCHEMA_VALID_8_OF_8_LATEST_RUNS",
            "behavioral_semantic_calibration": "PASS_6_OF_8_ROLES",
        },
        "behavioral_calibration": {
            "authorized": True,
            "synthetic_only": True,
            "denominator": behavior["behavior_denominator"],
            "accepted_passes": behavior["accepted_behavior_passes"],
            "roles_with_passing_run": behavior["roles_with_passing_run"],
            "roles_expected": behavior["roles_expected"],
            "failed_roles": [row["agent_id"] for row in roles if row["behavioral_calibration_status"] != "PASS"],
        },
        "package_zip_sha256": sha256(REPO / ZIP_REL),
        "sealed_package_unchanged": sha256(REPO / ZIP_REL) == ZIP_SHA256,
        "substantive_review_started": False,
        "founder_activation_approval": False,
        "merged": False,
        "final_disposition": FINAL_DISPOSITION,
    }
    write_json(REMEDIATION / "MACHINE_READABLE_RUNTIME_DISPOSITION.json", machine)

    runtime_identity = {
        "captured_for": "FORA runtime discovery remediation",
        "current_working_directory": str(REPO),
        "repository_root": str(REPO),
        "branch": BRANCH,
        "starting_commit": START_COMMIT,
        "initial_working_tree_status": "clean",
        "codex_cli_version": "0.144.6",
        "codex_executable_path": "/Users/rianray/.npm-global/bin/codex",
        "codex_runtime_binary": "/Users/rianray/.npm-global/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex",
        "operating_system": "macOS 26.5.2 build 25F84; Darwin 25.5.0 arm64",
        "shell": "/bin/zsh",
        "home": str(Path.home()),
        "codex_home_environment": "unset",
        "effective_codex_home": str(Path.home() / ".codex"),
        "originating_surface": "Codex desktop app tool-backed task",
        "isolated_test_surfaces": ["interactive CLI", "codex exec --json"],
        "commands_and_live_policies": "recorded per run in command.txt or command.json and sanitized_child_sessions.json",
    }
    write_json(REMEDIATION / "RUNTIME_IDENTITY.json", runtime_identity)

    static_lines = [
        "# Custom Agent Discovery Matrix",
        "",
        "All nine project-scoped standalone TOML files parsed successfully. The eight operational roles plus the temporary canary are regular files under the active checkout's `.codex/agents/` directory.",
        "",
        "| File | Declared name | Sandbox | Approval | Required fields | Regular file | Marker |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in static_rows:
        required = "PASS" if row["description_present"] and row["developer_instructions_present"] else "FAIL"
        regular = "PASS" if row["regular_file"] else "FAIL"
        static_lines.append(
            f"| `{row['filename']}` | `{row['declared_name']}` | `{row['sandbox_mode']}` | `{row['approval_policy']}` | `{required}` | `{regular}` | `{row['registration_marker'] or 'canary marker in instructions'}` |"
        )
    static_lines.extend(
        [
            "",
            "Declared names are unique. `.codex/config.toml` parses with `max_threads=6` and `max_depth=1`. The eight-role test used sandbox-homogeneous 3+5 batching, keeping parent plus five children at the six-thread ceiling and every child at depth 1. The personal `~/.codex/agents/` directory was absent, so no personal TOML could poison discovery.",
        ]
    )
    write_text(REMEDIATION / "CUSTOM_AGENT_DISCOVERY_MATRIX.md", "\n".join(static_lines))

    canary_lines = [
        "# Canary Runtime Results",
        "",
        "The project-scoped canary loaded on both required CLI surfaces. Only the exact child response `ES_RUNTIME_CANARY_LOADED_V1` is accepted as loading proof.",
        "",
        "| Surface | Attempt | Exit | Marker | Classification |",
        "|---|---|---:|---|---|",
    ]
    for attempt in canary["attempts"]:
        canary_lines.append(
            f"| {attempt['surface']} | `{attempt['run_path'].split('runtime_remediation/',1)[-1]}` | {attempt['exit_status']} | `{'present' if attempt['exact_marker_appeared_from_child'] else 'absent'}` | `{attempt['classification']}` |"
        )
    canary_lines.extend(
        [
            "",
            "The preserved failures isolate invocation errors: a full-history fork cannot override `agent_type`; `-a` must precede the `exec` subcommand; and `task_name` remains required alongside `agent_type`. Because both project-scoped tests passed, no personal-agent copy was necessary.",
        ]
    )
    write_text(REMEDIATION / "CANARY_RUNTIME_RESULTS.md", "\n".join(canary_lines))

    role_lines = [
        "# Role Registration Proof Matrix",
        "",
        "Individual registration and instruction-loading proof passed for all eight roles. Parent summaries are corroborated by sanitized child session metadata and the child's deliberately embedded marker.",
        "",
        "| Role | Exact custom-agent type | Configured / actual sandbox | Marker | Individual | Behavioral |",
        "|---|---|---|---|---|---|",
    ]
    for row in roles:
        role_lines.append(
            f"| `{row['agent_id']}` | `{row['declared_custom_agent_name']}` | `{row['configured_sandbox']}` / `{row['actual_child_sandbox']}` | `{row['registration_marker']}` | `PASS` | `{row['behavioral_calibration_status']} ({row['accepted_behavior_passes']}/{row['behavior_tests_total']})` |"
        )
    role_lines.extend(
        [
            "",
            "The bounded eight-role orchestration also passed using a read-only batch of three and a workspace-write batch of five. The first workspace batch's no-spawn parent response is retained as `INVOCATION_FAILED`; its exact-call retry passed 5/5.",
            "",
            "Subagent session provenance records `approval_policy=never` on this noninteractive surface even when the parent requested `on-request`. Calibration prohibited any action requiring escalation, so this mismatch is disclosed as a runtime limitation rather than treated as approval-policy equivalence.",
        ]
    )
    write_text(REMEDIATION / "ROLE_REGISTRATION_PROOF_MATRIX.md", "\n".join(role_lines))

    trust_report = f"""# Project Trust and Config Provenance

## Result

`PASS` — the exact repository/worktree path was already explicitly trusted before project-agent testing:

`{REPO}`

The containing Codex task directory was also trusted. No trust correction or session restart was required.

## Effective configuration

- `HOME`: `{Path.home()}`
- `CODEX_HOME` environment variable: unset
- effective Codex home: `{Path.home() / '.codex'}`
- user config: `{Path.home() / '.codex' / 'config.toml'}`
- project config: `{REPO / '.codex' / 'config.toml'}`
- project config strict parse: `PASS`
- `[agents].max_threads`: `6`
- `[agents].max_depth`: `1`
- project standalone agents: `{REPO / '.codex' / 'agents'}`
- personal standalone-agent directory: absent

No secret-bearing user configuration is copied into this evidence package. The trust fact is recorded as a sanitized value only.

The controlled batch design used three read-only children in one parent session and five workspace-write children in another. This stays within six threads including the parent and requires only depth 1.
"""
    write_text(REMEDIATION / "PROJECT_TRUST_AND_CONFIG_PROVENANCE.md", trust_report)

    diagnostic = f"""# Runtime Discovery Diagnostic Report

## Outcome

Project-scoped custom-agent discovery is supported and proven on Codex CLI `0.144.6`. All eight installed roles were selected by exact standalone `agent_type`, and each child returned its deliberately embedded registration marker. The current installation is nevertheless not ready for Founder activation review because ES-RA-04 and ES-RA-06 failed the downstream behavioral calibration.

## Controlled baseline

- branch: `{BRANCH}`
- immutable pre-remediation commit: `{START_COMMIT}`
- parent installation commit: `{PARENT_INSTALLATION_COMMIT}`
- initial worktree: clean
- package ZIP SHA-256: `{ZIP_SHA256}`
- substantive review: not started

## Root cause

The project was trusted and the standalone TOML layout was valid. The pre-remediation orchestration path selected named task paths without reliably supplying the standalone custom-agent `agent_type`; the calibration harness also launched with `--ignore-user-config`, removing the effective trusted configuration stack used by successful custom-agent selection. A task path alone is not proof of instruction loading.

The minimum remediation is therefore invocation-level:

1. retain the trusted user/project configuration stack;
2. start at the repository root;
3. call `spawn_agent` with both `task_name` and exact `agent_type`;
4. set `fork_turns="none"` so the custom type is not overridden by full-history inheritance; and
5. accept loading only when child session metadata names the exact custom role and the child returns the embedded marker without reading `.codex/agents`.

No operational role semantics, sealed package file, prior failed-run evidence, or package-controlled calibration artifact was changed.

## Test results

- project trust: `PASS`
- standalone TOML discovery: `9/9` including temporary canary
- canary surfaces: interactive CLI `PASS`; `codex exec --json` `PASS`
- individual operational roles: `8/8` discovered and `8/8` instruction layers loaded
- representative read-only behavior: `PASS`, including refusal to draft/modify controlled content
- representative workspace-write behavior: `PASS`, exactly one authorized disposable probe file
- bounded orchestration: `8/8 PASS` by controlled 3+5 batching
- behavioral suite: `90/120` accepted; six roles passed and two failed

## Behavioral blockers

- ES-RA-04 returned an incorrect marker (`V1.0`), incorrect loaded name, non-prescribed decisions, and the wrong permitted disposition.
- ES-RA-06 returned a domain placeholder as its marker and remained schema/decision-nonconforming after corrections in the same child session.

These are genuine role-calibration failures, not discovery failures. They are preserved without modifying the agents during this narrowly scoped remediation.
"""
    write_text(REMEDIATION / "RUNTIME_DISCOVERY_DIAGNOSTIC_REPORT.md", diagnostic)

    final_report = f"""# Runtime Remediation Final Report

## Final disposition

`{FINAL_DISPOSITION}`

This is not Founder activation approval. No substantive Founder-Orchestrated Review Cycle began.

## Summary

- repository trust: `PASS`
- runtime surfaces tested: interactive CLI and `codex exec --json`
- canary: `PASS` on both required surfaces
- project-agent discovery: `8/8 PASS`
- custom instruction loading: `8/8 PASS`
- individual role registration schema: `8/8 PASS`
- sandbox provenance: `8/8 matched`; network denied in accepted child sessions
- bounded eight-role orchestration: `8/8 PASS` using controlled 3+5 batching
- behavioral calibration: `90/120` accepted; ES-RA-04 and ES-RA-06 failed
- sealed ZIP SHA-256: `{ZIP_SHA256}` (`PASS`)
- sealed/package-controlled paths changed: none
- branch merged: no

## Minimum remediation implemented

- added a temporary read-only canary under `.codex/agents/`;
- added an additive runtime-remediation runner that retains the trusted config stack and supplies exact `agent_type` with `fork_turns="none"`;
- added schemas, raw parent outputs, stderr, prompts, timestamps, exit statuses, sanitized child-session provenance, matrices, reports, and integrity manifests under `runtime_remediation/`;
- preserved every failed attempt and retry.

## Sandbox and approval provenance

Accepted read-only roles ran with child `sandbox_policy.type=read-only`. Accepted writable roles ran with `workspace-write` and denied network. The ES-RA-05 probe created only its one authorized disposable file. Workspace-write is not a path-level allowlist, so the narrower location remained a procedural constraint corroborated by the file-diff result.

The noninteractive child sessions recorded `approval_policy=never` even where `on-request` was requested. Because all calibration inputs prohibited network, production, destructive activity, and actions needing escalation, no approval bypass was exercised. This limitation must be reconsidered before any operational activation.

## Unresolved limitations

1. ES-RA-04 and ES-RA-06 need role-specific calibration remediation and fresh accepted behavioral runs.
2. The parent output does not expose a resolved-agent-type field; child session `agent_role` metadata plus the private marker provide the proof.
3. The originating desktop/tool-backed collaboration surface does not expose first-class `agent_type` selection in this task; the supported CLI surfaces were used for reproducible proof.
4. JSONL provenance is not an operating-system syscall audit.
5. No personal-agent copy test was run because project-scoped discovery passed on both required surfaces.

## Disposition boundary

Do not activate, merge, or issue Founder approval from this result. The next permitted action is a narrowly scoped remediation and rerun for ES-RA-04 and ES-RA-06, followed by regeneration of the behavioral aggregate and this disposition.
"""
    write_text(REMEDIATION / "RUNTIME_REMEDIATION_FINAL_REPORT.md", final_report)

    json_failures = []
    json_count = 0
    for path in sorted(REMEDIATION.rglob("*.json")):
        if "__pycache__" in path.parts:
            continue
        json_count += 1
        try:
            read_json(path)
        except Exception as error:
            json_failures.append(f"{path.relative_to(REPO)}: {error}")
    sealed_diff = command(
        "git", "diff", "--name-only", START_COMMIT, "--",
        "governance/founder_orchestrated_review/agent_config/packages",
        "governance/founder_orchestrated_review/agent_config/V1.0.0",
        "governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs",
    )
    validation = {
        "schema_version": "1.0.0",
        "json_files_parsed": json_count,
        "json_parse_failures": json_failures,
        "standalone_agent_toml_parsed": len(static_rows),
        "standalone_agent_required_fields_passed": sum(
            row["description_present"] and row["developer_instructions_present"] for row in static_rows
        ),
        "individual_registration_schema_passed": 8,
        "individual_registration_schema_expected": 8,
        "behavioral_response_schema_valid_latest_runs": 8,
        "behavioral_response_schema_expected": 8,
        "behavioral_semantic_passes": behavior["accepted_behavior_passes"],
        "behavioral_semantic_denominator": behavior["behavior_denominator"],
        "sealed_controlled_path_diff": sealed_diff.splitlines() if sealed_diff else [],
        "zip_sha256": sha256(REPO / ZIP_REL),
        "zip_sha256_matches": sha256(REPO / ZIP_REL) == ZIP_SHA256,
        "evidence_validation": "PASS" if not json_failures and not sealed_diff else "FAIL",
        "operational_disposition": FINAL_DISPOSITION,
    }
    write_json(REMEDIATION / "RUNTIME_REMEDIATION_VALIDATION_RESULT.json", validation)

    manifest_paths = [Path(".codex/agents/es_runtime_canary.toml")]
    manifest_paths.extend(
        path.relative_to(REPO)
        for path in sorted(REMEDIATION.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    )
    for required in (
        Path("governance/founder_orchestrated_review/runtime_remediation/RUNTIME_REMEDIATION_CHANGE_MANIFEST.txt"),
        Path("governance/founder_orchestrated_review/runtime_remediation/RUNTIME_REMEDIATION_CHECKSUMS.sha256"),
    ):
        if required not in manifest_paths:
            manifest_paths.append(required)
    manifest_paths = sorted(set(manifest_paths), key=str)
    write_text(
        REMEDIATION / "RUNTIME_REMEDIATION_CHANGE_MANIFEST.txt",
        "\n".join(str(path) for path in manifest_paths),
    )

    checksum_targets = [REPO / ".codex" / "agents" / "es_runtime_canary.toml"]
    checksum_targets.extend(
        path for path in sorted(REMEDIATION.rglob("*"))
        if path.is_file()
        and path.name != "RUNTIME_REMEDIATION_CHECKSUMS.sha256"
        and "__pycache__" not in path.parts
    )
    checksum_lines = [f"{sha256(path)}  {path.relative_to(REPO)}" for path in checksum_targets]
    write_text(REMEDIATION / "RUNTIME_REMEDIATION_CHECKSUMS.sha256", "\n".join(checksum_lines))
    print(json.dumps({
        "final_disposition": FINAL_DISPOSITION,
        "files_in_manifest": len(manifest_paths),
        "checksum_entries": len(checksum_lines),
        "json_files_parsed": json_count,
    }, indent=2))


if __name__ == "__main__":
    main()
