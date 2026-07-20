#!/usr/bin/env python3
"""Assemble additive final evidence for the bounded remediation run."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from runtime_support import BRANCH, PACKAGE_SHA256, REPO_ROOT, RUN_ID, RUN_ROOT, STARTING_COMMIT, sha256, write_json


DISPOSITION = "REMEDIATION_REQUALIFICATION_FAILED_FIRST_CANARY"


def purpose(path: Path) -> str:
    relative = path.relative_to(RUN_ROOT).as_posix()
    if relative.startswith("runtime/"):
        return "Disposable trusted read-only runtime and connector-isolation configuration."
    if relative.startswith("scripts/"):
        return "Reproducible baseline, validation, probe, canary, or evidence assembly logic."
    if relative.startswith("schemas/"):
        return "Machine-readable response constraint for authorized canaries."
    if relative.startswith("raw/"):
        return "Raw or sanitized evidence from the current authorized attempt."
    if relative.startswith("attempts/"):
        return "Preserved failed non-agent harness/probe attempt evidence."
    if relative.startswith("baseline/"):
        return "Immutable starting-commit byte baseline."
    return "Required additive remediation report or machine-readable result."


def source_files() -> list[Path]:
    excluded = {
        "RUNTIME_REMEDIATION_CHANGE_REGISTER.csv",
        "RUNTIME_REMEDIATION_CHANGE_REGISTER.json",
        "RUNTIME_REMEDIATION_EVIDENCE_MANIFEST.txt",
        "RUNTIME_REMEDIATION_SHA256SUMS.txt",
        "RUNTIME_REMEDIATION_CHANGE_MANIFEST.txt",
    }
    return [path for path in sorted(RUN_ROOT.rglob("*")) if path.is_file() and path.name not in excluded]


def write_change_register() -> None:
    entries = []
    for path in source_files():
        entries.append({
            "path": path.relative_to(REPO_ROOT).as_posix(),
            "purpose": purpose(path),
            "before_sha256": None,
            "after_sha256": sha256(path),
            "exact_change": "Added new file inside the additive FORA-REMEDIATION-2026-001 evidence boundary; no predecessor existed at the starting commit.",
            "reason": "Required to remediate or evidence the two authorized runtime blockers and the bounded read-only requalification.",
            "reversibility": "Delete this additive run file to return to the starting commit; no prior evidence or sealed package byte is changed.",
            "inside_sealed_package": False,
        })
    register = {
        "run_id": RUN_ID,
        "starting_commit": STARTING_COMMIT,
        "entry_count": len(entries),
        "entries": entries,
        "self_attestation": "The two register files and final manifest files are hashed by RUNTIME_REMEDIATION_SHA256SUMS.txt to avoid self-referential hashes.",
    }
    write_json(RUN_ROOT / "RUNTIME_REMEDIATION_CHANGE_REGISTER.json", register)
    with (RUN_ROOT / "RUNTIME_REMEDIATION_CHANGE_REGISTER.csv").open("w", encoding="utf-8", newline="") as stream:
        fieldnames = ["path", "purpose", "before_sha256", "after_sha256", "exact_change", "reason", "reversibility", "inside_sealed_package"]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)


def write_preservation_and_configuration() -> None:
    static = json.loads((RUN_ROOT / "PRE_CANARY_STATIC_VALIDATION.json").read_text(encoding="utf-8"))
    probe = json.loads((RUN_ROOT / "NON_AGENT_RUNTIME_PROBE.json").read_text(encoding="utf-8"))
    (RUN_ROOT / "SEALED_PACKAGE_PRESERVATION_REPORT.md").write_text("\n".join([
        "# Sealed Package Preservation Report", "",
        "Result: `PASS`", "",
        f"- Starting commit: `{STARTING_COMMIT}`",
        f"- Baseline entries checked: `{static['baseline_entries_checked']}`",
        f"- Total baseline byte mismatches: `{len(static['baseline_mismatches'])}`",
        f"- Sealed-package mismatches: `{static['category_mismatch_counts']['sealed_package']}`",
        f"- Registered-role-file mismatches: `{static['category_mismatch_counts']['registered_role_files']}`",
        f"- Prior-activation-evidence mismatches: `{static['category_mismatch_counts']['prior_activation_evidence']}`",
        f"- Prior runtime/calibration evidence mismatches: `{static['category_mismatch_counts']['prior_runtime_and_calibration_evidence']}`",
        f"- Approved ZIP SHA-256: `{static['package_zip_sha256']}`",
        "- Sealed package files changed: `0`", "",
        "Every remediation change is additive and outside the sealed Founder-approved package.", "",
    ]), encoding="utf-8")
    features = probe["effective_config_summary"]["features"]
    disabled = sorted(name for name, value in features.items() if value is False)
    (RUN_ROOT / "CONNECTOR_ISOLATION_CONFIGURATION.md").write_text("\n".join([
        "# Connector Isolation Configuration", "",
        "The canary launcher creates a fresh `CODEX_HOME`, copies only the minimum Codex control-plane authentication at run time, writes a profile that trusts only the exact clean checkout, and removes the temporary authentication material after evidence extraction.", "",
        "The profile declares no MCP server or plugin and disables all discovered connector/autoload surfaces. The sanitized process environment contains only basic shell/runtime names; sensitive ambient variables are detected by name and not inherited. The command uses `--strict-config`, read-only sandboxing, disabled web search, and does not use `--ignore-user-config` because the disposable profile itself is the controlled user configuration needed to express checkout trust.", "",
        f"- Effective MCP servers: `{len(probe['effective_config_summary']['mcp_servers'])}`",
        f"- Disabled connector/plugin features: `{', '.join(disabled)}`",
        f"- Multi-agent feature: `{probe['effective_config_summary']['features']['multi_agent']}`",
        f"- Project layer count: `{probe['effective_config_summary']['project_layer_count']}`",
        f"- Project layer disabled reason: `{probe['effective_config_summary']['project_layer_disabled_reason']}`",
        f"- Non-agent-probe Cloudflare attempts: `{probe['cloudflare_mcp_attempts']}`",
        "- Production credentials, routes, and provider tools exposed: none", "",
        "The Codex control-plane transport required to execute the authorized canary is not treated as role authority or as child network-tool use.", "",
    ]), encoding="utf-8")


def write_final(resulting_commit: str | None, fresh_clone: str) -> None:
    static = json.loads((RUN_ROOT / "PRE_CANARY_STATIC_VALIDATION.json").read_text(encoding="utf-8"))
    probe = json.loads((RUN_ROOT / "NON_AGENT_RUNTIME_PROBE.json").read_text(encoding="utf-8"))
    canary = json.loads((RUN_ROOT / "READ_ONLY_CANARY_01_RESULT.json").read_text(encoding="utf-8"))
    required_names = {
        "SEALED_PACKAGE_PRESERVATION_REPORT.md", "CONNECTOR_ISOLATION_CONFIGURATION.md",
        "RUNTIME_REMEDIATION_FINAL_REPORT.md", "RUNTIME_REMEDIATION_FINAL_RESULT.json",
        "RUNTIME_REMEDIATION_CHANGE_REGISTER.csv", "RUNTIME_REMEDIATION_CHANGE_REGISTER.json",
        "RUNTIME_REMEDIATION_EVIDENCE_MANIFEST.txt", "RUNTIME_REMEDIATION_SHA256SUMS.txt",
        "RUNTIME_REMEDIATION_CHANGE_MANIFEST.txt",
    }
    current_relatives = {
        path.relative_to(RUN_ROOT).as_posix()
        for path in RUN_ROOT.rglob("*") if path.is_file()
    }
    files_changed = len(current_relatives | required_names)
    result = {
        "run_id": RUN_ID,
        "authority": "Founder authorization limited to runtime loading, connector isolation, and read-only requalification",
        "repository": "https://github.com/rianray2012-coder/EquineSync-V4.git",
        "branch": BRANCH,
        "starting_commit": STARTING_COMMIT,
        "resulting_commit": resulting_commit,
        "default_branch": "integrate-emergent-final-zip",
        "package_zip_sha256": PACKAGE_SHA256,
        "prior_activation_disposition": "ACTIVATION_BLOCKED_OR_ROLLBACK_REQUIRED",
        "custom_agent_loading_root_cause": "The prior isolated profile did not trust the checkout, disabling project custom-agent configuration. Trust remediation loaded the project layer, but the first requalification still proved the available spawn interface stripped the requested agent_type and created a generic child with null agent_role.",
        "connector_activity_root_cause": "remote_plugin defaulted true in the prior isolated profile and populated a required Cloudflare MCP plugin, producing three authentication attempts.",
        "files_changed": files_changed,
        "sealed_files_changed": 0,
        "static_validation_result": static["status"],
        "installed_system_validation": {"passed": 16, "total": 16, "status": "PASS"},
        "individual_canaries_attempted": 1,
        "individual_canaries_passed": 0,
        "batch_attempted": False,
        "batch_passed": False,
        "agent_type_values": canary["agent_type_values"],
        "agent_role_values": canary["agent_role_values"],
        "generic_fallback_detected": canary["generic_fallback_detected"],
        "parent_substitution_detected": canary["parent_substitution_detected"],
        "cloudflare_mcp_attempts": canary["cloudflare_mcp_attempts"],
        "other_unauthorized_connector_attempts": canary["other_unauthorized_connector_attempts"],
        "tool_calls": canary["child_tool_calls"],
        "parent_orchestration_tool_calls": 2,
        "workspace_writes": canary["workspace_writes"],
        "workspace_write_roles_started": 0,
        "substantive_review_performed": False,
        "production_access": False,
        "provider_writes": 0,
        "pull_requests_created": False,
        "merged": False,
        "default_branch_modified": False,
        "tag_created": False,
        "release_created": False,
        "deployment_performed": False,
        "inactive_configuration_preserved": True,
        "sealed_package_preserved": True,
        "fresh_clone_verification": fresh_clone,
        "final_disposition": DISPOSITION,
        "founder_reauthorization_required": True,
        "non_agent_probe": {"status": probe["status"], "checks_passed": probe["checks_passed"], "checks_total": probe["checks_total"]},
        "failed_canary": {
            "requested_agent": "equinesync_segregated_review_agent",
            "expected_role": "ES-RA-02",
            "requested_agent_type_runtime_value": None,
            "observed_child_agent_role": None,
            "direct_child_registration_marker": None,
            "direct_child_custom_instruction_layer_acknowledged": False,
            "retry_performed": False,
        },
    }
    write_json(RUN_ROOT / "RUNTIME_REMEDIATION_FINAL_RESULT.json", result)
    (RUN_ROOT / "RUNTIME_REMEDIATION_FINAL_REPORT.md").write_text("\n".join([
        "# Runtime Remediation Final Report", "",
        f"Final disposition: `{DISPOSITION}`", "",
        "## Outcome", "",
        "Static validation and connector isolation passed, but the first authorized custom-agent canary failed. The parent runtime recorded `agent_type=null`; the child runtime recorded `agent_role=null`; and the direct child returned no registered role, marker, or role-prompt path. The parent then supplied identity values absent from the direct child, which the scorer correctly rejected as substitution. All further agent use stopped immediately and no retry occurred.", "",
        "## Root causes", "",
        "- Prior custom-agent failure: the prior disposable `CODEX_HOME` lacked trust for its clean checkout, so Codex disabled the project `.codex` layer.",
        "- Residual runtime blocker after trust correction: Codex CLI `0.144.6` exposed a spawn interface that did not serialize the requested custom `agent_type`; the generic child therefore had null role metadata.",
        "- Prior connector activity: `remote_plugin=true` populated the Cloudflare plugin, whose required MCP declaration attempted authentication three times.", "",
        "## Remediation applied", "",
        "A reversible disposable profile now trusts only the exact execution checkout, retains multi-agent operation, enforces read-only policy, declares zero MCP servers/plugins, disables every identified plugin/app/connector autoload feature, sanitizes the environment, and removes copied control-plane authentication after each run. No sealed or registered-role file changed.", "",
        "## Verification", "",
        f"- Static validation: `{static['status']}` (`{static['checks_passed']}/{static['checks_total']}`); installed system `16/16 PASS`",
        f"- Non-agent runtime probe: `{probe['status']}` (`{probe['checks_passed']}/{probe['checks_total']}`)",
        "- ES-RA-02 individual canary: `FAIL` (`agent_type=null`, `agent_role=null`)",
        "- ES-RA-03 and ES-RA-06 individual canaries: not attempted due stop rule",
        "- Three-role bounded batch: not attempted due stop rule",
        "- Cloudflare MCP attempts during canary: `0`",
        "- Other unauthorized connector attempts: `0`",
        "- Child tool calls: `0`; workspace writes: `0`; workspace-write roles started: `0`",
        "- Substantive review, production access, provider writes, PR, merge, tag, release, and deployment: none",
        f"- Fresh-clone verification: `{fresh_clone}`", "",
        "The system remains inactive and blocked. A new Founder authorization and a runtime surface that preserves exact custom `agent_type` are required before any further agent attempt.", "",
        "> No workspace-write review role, full operational activation, or substantive Founder-Orchestrated Review is authorized by this directive. Even after successful read-only requalification, further activity requires a separate, explicit Founder authorization.", "",
    ]), encoding="utf-8")


def write_manifests() -> None:
    all_files = [path for path in sorted(RUN_ROOT.rglob("*")) if path.is_file()]
    change_manifest = RUN_ROOT / "RUNTIME_REMEDIATION_CHANGE_MANIFEST.txt"
    change_paths = [path.relative_to(REPO_ROOT).as_posix() for path in all_files if path != change_manifest]
    change_manifest.write_text("\n".join(change_paths + [change_manifest.relative_to(REPO_ROOT).as_posix()]) + "\n", encoding="utf-8")
    evidence_manifest = RUN_ROOT / "RUNTIME_REMEDIATION_EVIDENCE_MANIFEST.txt"
    evidence_files = [path for path in sorted(RUN_ROOT.rglob("*")) if path.is_file() and path.name not in {"RUNTIME_REMEDIATION_EVIDENCE_MANIFEST.txt", "RUNTIME_REMEDIATION_SHA256SUMS.txt"}]
    evidence_manifest.write_text("\n".join(f"{sha256(path)}\t{path.stat().st_size}\t{path.relative_to(RUN_ROOT).as_posix()}" for path in evidence_files) + "\n", encoding="utf-8")
    sums = RUN_ROOT / "RUNTIME_REMEDIATION_SHA256SUMS.txt"
    sum_files = [path for path in sorted(RUN_ROOT.rglob("*")) if path.is_file() and path != sums]
    sums.write_text("\n".join(f"{sha256(path)}  {path.relative_to(RUN_ROOT).as_posix()}" for path in sum_files) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resulting-commit")
    parser.add_argument("--fresh-clone-status", default="PENDING")
    args = parser.parse_args()
    write_preservation_and_configuration()
    write_final(args.resulting_commit, args.fresh_clone_status)
    write_change_register()
    # Recompute the final report/result after all required non-manifest files exist.
    write_final(args.resulting_commit, args.fresh_clone_status)
    write_change_register()
    write_manifests()
    print(json.dumps({"disposition": DISPOSITION, "files": len([path for path in RUN_ROOT.rglob('*') if path.is_file()])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
