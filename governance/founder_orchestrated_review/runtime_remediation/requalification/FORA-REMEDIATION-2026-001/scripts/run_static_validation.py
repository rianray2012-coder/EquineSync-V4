#!/usr/bin/env python3
"""Run the required pre-canary static checks without changing prior evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from runtime_support import BRANCH, PACKAGE_SHA256, REPO_ROOT, RUN_ROOT, STARTING_COMMIT, git, sha256, write_json


PACKAGE = Path("governance/founder_orchestrated_review/agent_config/packages/EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip")
PACKAGE_CHECKSUM = PACKAGE.with_name(PACKAGE.name + ".sha256")
SEALED = Path("governance/founder_orchestrated_review/agent_config/V1.0.0")
BASELINE = RUN_ROOT / "baseline" / "BASELINE_BYTE_MANIFEST.json"
RAW = RUN_ROOT / "raw" / "static_validation"
RESULT = RUN_ROOT / "PRE_CANARY_STATIC_VALIDATION.json"
REPORT = RUN_ROOT / "PRE_CANARY_STATIC_VALIDATION.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation-clone", required=True, type=Path)
    parser.add_argument("--python", default=Path(sys.executable), type=Path)
    args = parser.parse_args()
    clone = args.validation_clone.resolve()
    RAW.mkdir(parents=True, exist_ok=False)

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    mismatches = []
    for entry in baseline["entries"]:
        path = REPO_ROOT / entry["path"]
        actual = sha256(path) if path.is_file() else None
        if actual != entry["sha256"]:
            mismatches.append({"path": entry["path"], "expected": entry["sha256"], "actual": actual})

    # Preserve a virtual-environment launcher path; resolving its symlink would
    # bypass the venv and therefore its declared validation dependencies.
    validator_python = args.python.expanduser().absolute()
    command = [str(validator_python), "governance/founder_orchestrated_review/validation/validate_installed_agent_system.py"]
    codex_launcher = shutil.which("codex")
    if not codex_launcher:
        raise RuntimeError("codex executable unavailable for dependency provenance")
    validator_path = f"{validator_python.parent}:{Path(codex_launcher).parent}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    completed = subprocess.run(command, cwd=clone, capture_output=True, text=True, check=False, env={"PATH": validator_path, "PYTHONDONTWRITEBYTECODE": "1", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"})
    (RAW / "installed_system_validator.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (RAW / "installed_system_validator.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    (RAW / "installed_system_validator.command.json").write_text(json.dumps({"argv": command, "cwd": str(clone), "environment_variable_names_only": ["LANG", "LC_ALL", "PATH", "PYTHONDONTWRITEBYTECODE"], "dependency_source": "validation/requirements.txt installed into a disposable validation-only virtual environment"}, indent=2) + "\n", encoding="utf-8")
    generated_result = clone / "governance/founder_orchestrated_review/validation/INSTALLED_SYSTEM_VALIDATION_RESULT.json"
    installed = json.loads(generated_result.read_text(encoding="utf-8")) if generated_result.is_file() else {}
    for name in ("INSTALLED_SYSTEM_VALIDATION_RESULT.json", "INSTALLED_SYSTEM_VALIDATION_REPORT.md", "INSTALLED_SYSTEM_VALIDATION_COMMAND_LOG.txt", "INSTALLED_SYSTEM_VALIDATION_DEPENDENCIES.json"):
        source = clone / "governance/founder_orchestrated_review/validation" / name
        if source.is_file():
            shutil.copyfile(source, RAW / name)

    package = REPO_ROOT / PACKAGE
    checksum_line = (REPO_ROOT / PACKAGE_CHECKSUM).read_text(encoding="utf-8").strip()
    expected_line = f"{PACKAGE_SHA256}  {PACKAGE.name}"
    sealed_validation = subprocess.run(
        [sys.executable, "scripts/validate_package.py"], cwd=REPO_ROOT / SEALED,
        capture_output=True, text=True, check=False,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin", "PYTHONDONTWRITEBYTECODE": "1", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
    )
    (RAW / "sealed_package_validator.stdout.txt").write_text(sealed_validation.stdout, encoding="utf-8")
    (RAW / "sealed_package_validator.stderr.txt").write_text(sealed_validation.stderr, encoding="utf-8")

    category_mismatches = {}
    for category in sorted({entry["category"] for entry in baseline["entries"]}):
        category_mismatches[category] = sum(item["path"] == entry["path"] for item in mismatches for entry in baseline["entries"] if entry["category"] == category)
    checks = {
        "validation_clone_head_is_starting_commit": git(clone, "rev-parse", "HEAD").stdout.strip() == STARTING_COMMIT,
        "validation_clone_branch_is_authorized": git(clone, "branch", "--show-current").stdout.strip() == BRANCH,
        "installed_system_validator_exit_zero": completed.returncode == 0,
        "installed_system_validation_pass": installed.get("status") == "PASS",
        "installed_system_validation_16_of_16": installed.get("summary", {}).get("checks") == 16 and installed.get("summary", {}).get("passed") == 16 and installed.get("summary", {}).get("failed") == 0,
        "approved_package_zip_hash": sha256(package) == PACKAGE_SHA256,
        "approved_package_checksum_line_exact": checksum_line == expected_line,
        "sealed_package_internal_validation": sealed_validation.returncode == 0 and "PACKAGE VALIDATION PASSED" in sealed_validation.stdout,
        "baseline_manifest_pass": baseline.get("status") == "PASS",
        "baseline_bytes_preserved": mismatches == [],
        "sealed_package_preserved": category_mismatches.get("sealed_package", 1) == 0,
        "registered_role_files_preserved": category_mismatches.get("registered_role_files", 1) == 0,
        "prior_activation_evidence_preserved": category_mismatches.get("prior_activation_evidence", 1) == 0,
        "prior_runtime_and_calibration_evidence_preserved": category_mismatches.get("prior_runtime_and_calibration_evidence", 1) == 0,
        "inactive_configuration_preserved": category_mismatches.get("runtime_or_launcher_configuration", 1) == 0 and category_mismatches.get("orchestration_configuration", 1) == 0,
        "workspace_write_roles_not_run": True,
        "substantive_review_not_run": True,
    }
    result = {
        "run_id": "FORA-REMEDIATION-2026-001",
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "baseline_entries_checked": len(baseline["entries"]),
        "baseline_mismatches": mismatches,
        "category_mismatch_counts": category_mismatches,
        "installed_system_validation": installed.get("summary"),
        "package_zip_sha256": sha256(package),
        "sealed_package_validator_exit_code": sealed_validation.returncode,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "failure_disposition": None if all(checks.values()) else "REMEDIATION_FAILED_STATIC_VALIDATION",
    }
    write_json(RESULT, result)
    lines = [
        "# Pre-Canary Static Validation", "",
        f"Result: `{result['status']}` (`{result['checks_passed']}/{result['checks_total']}` checks)", "",
        f"- Installed-system validation: `{installed.get('summary', {}).get('passed', 0)}/{installed.get('summary', {}).get('checks', 0)} PASS`",
        f"- Immutable baseline entries checked: `{len(baseline['entries'])}`",
        f"- Byte mismatches: `{len(mismatches)}`",
        f"- Approved package ZIP SHA-256: `{result['package_zip_sha256']}`",
        f"- Sealed package validation: `{'PASS' if sealed_validation.returncode == 0 else 'FAIL'}`",
        "- Workspace-write roles: not run",
        "- Substantive review: not run", "",
        "A failing result prohibits every agent canary and requires `REMEDIATION_FAILED_STATIC_VALIDATION`.", "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": f"{result['checks_passed']}/{result['checks_total']}"}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
