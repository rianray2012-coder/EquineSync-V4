#!/usr/bin/env python3
"""Verify the pushed remediation evidence in a clean GitHub clone."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from runtime_support import BRANCH, PACKAGE_SHA256, REPO_ROOT, RUN_ID, RUN_ROOT, sha256, write_json


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clone", required=True, type=Path)
    parser.add_argument("--target-commit", required=True)
    parser.add_argument("--pull-request-count", required=True, type=int)
    args = parser.parse_args()
    clone = args.clone.resolve()
    target = args.target_commit
    clone_run = clone / RUN_ROOT.relative_to(REPO_ROOT)

    checksum_failures = []
    checksum_lines = (clone_run / "RUNTIME_REMEDIATION_SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    for line in checksum_lines:
        expected, relative = line.split("  ", 1)
        path = clone_run / relative
        actual = sha256(path) if path.is_file() else None
        if actual != expected:
            checksum_failures.append({"path": relative, "expected": expected, "actual": actual})

    manifest_failures = []
    manifest_lines = (clone_run / "RUNTIME_REMEDIATION_EVIDENCE_MANIFEST.txt").read_text(encoding="utf-8").splitlines()
    for line in manifest_lines:
        expected, size, relative = line.split("\t", 2)
        path = clone_run / relative
        actual = sha256(path) if path.is_file() else None
        actual_size = path.stat().st_size if path.is_file() else None
        if actual != expected or actual_size != int(size):
            manifest_failures.append({"path": relative, "expected_sha256": expected, "actual_sha256": actual, "expected_bytes": int(size), "actual_bytes": actual_size})

    baseline = json.loads((clone_run / "baseline" / "BASELINE_BYTE_MANIFEST.json").read_text(encoding="utf-8"))
    baseline_failures = []
    for entry in baseline["entries"]:
        path = clone / entry["path"]
        actual = sha256(path) if path.is_file() else None
        if actual != entry["sha256"]:
            baseline_failures.append({"path": entry["path"], "expected": entry["sha256"], "actual": actual})

    package = clone / "governance/founder_orchestrated_review/agent_config/packages/EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip"
    final = json.loads((clone_run / "RUNTIME_REMEDIATION_FINAL_RESULT.json").read_text(encoding="utf-8"))
    required = [
        "RUNTIME_REMEDIATION_AUTHORITY.md", "RUNTIME_REMEDIATION_BASELINE.md", "RUNTIME_REMEDIATION_BASELINE.json",
        "CUSTOM_AGENT_LOADING_ROOT_CAUSE_ANALYSIS.md", "CONNECTOR_ISOLATION_ROOT_CAUSE_ANALYSIS.md",
        "RUNTIME_REMEDIATION_CHANGE_REGISTER.csv", "RUNTIME_REMEDIATION_CHANGE_REGISTER.json",
        "SEALED_PACKAGE_PRESERVATION_REPORT.md", "CONNECTOR_ISOLATION_CONFIGURATION.md",
        "PRE_CANARY_STATIC_VALIDATION.md", "PRE_CANARY_STATIC_VALIDATION.json", "NON_AGENT_RUNTIME_PROBE.md",
        "READ_ONLY_CANARY_01_REPORT.md", "READ_ONLY_CANARY_01_RESULT.json",
        "RUNTIME_REMEDIATION_FINAL_REPORT.md", "RUNTIME_REMEDIATION_FINAL_RESULT.json",
        "RUNTIME_REMEDIATION_EVIDENCE_MANIFEST.txt", "RUNTIME_REMEDIATION_SHA256SUMS.txt",
        "RUNTIME_REMEDIATION_CHANGE_MANIFEST.txt",
    ]
    default_fetch = git(clone, "fetch", "origin", "integrate-emergent-final-zip:refs/remotes/origin/integrate-emergent-final-zip")
    containment = git(clone, "merge-base", "--is-ancestor", target, "refs/remotes/origin/integrate-emergent-final-zip")
    tags = git(clone, "tag", "--contains", target).stdout.splitlines()
    checks = {
        "fresh_clone_head_exact": git(clone, "rev-parse", "HEAD").stdout.strip() == target,
        "authorized_branch": git(clone, "branch", "--show-current").stdout.strip() == BRANCH,
        "working_tree_clean": git(clone, "status", "--porcelain=v1", "--untracked-files=all").stdout == "",
        "checksum_manifest_pass": checksum_failures == [],
        "evidence_manifest_pass": manifest_failures == [],
        "baseline_617_entries": baseline.get("entry_count") == 617,
        "immutable_baseline_pass": baseline_failures == [],
        "approved_package_hash": sha256(package) == PACKAGE_SHA256,
        "required_evidence_present": all((clone_run / name).is_file() for name in required),
        "final_disposition_consistent": final.get("final_disposition") == "REMEDIATION_REQUALIFICATION_FAILED_FIRST_CANARY",
        "canary_counts_consistent": final.get("individual_canaries_attempted") == 1 and final.get("individual_canaries_passed") == 0 and final.get("batch_attempted") is False,
        "no_workspace_write_or_substantive_review": final.get("workspace_write_roles_started") == 0 and final.get("workspace_writes") == 0 and final.get("substantive_review_performed") is False,
        "default_branch_fetch_pass": default_fetch.returncode == 0,
        "target_not_in_default_branch": containment.returncode == 1,
        "open_pull_request_count_zero": args.pull_request_count == 0,
        "no_tag_contains_target": tags == [],
        "sealed_package_preserved": final.get("sealed_package_preserved") is True and baseline_failures == [],
        "no_merge_release_or_deployment_recorded": final.get("merged") is False and final.get("release_created") is False and final.get("deployment_performed") is False,
    }
    result = {
        "run_id": RUN_ID,
        "verified_commit": target,
        "branch": BRANCH,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checksum_entries": len(checksum_lines),
        "checksum_failures": checksum_failures,
        "evidence_manifest_entries": len(manifest_lines),
        "evidence_manifest_failures": manifest_failures,
        "baseline_entries": baseline.get("entry_count"),
        "baseline_failures": baseline_failures,
        "package_zip_sha256": sha256(package),
        "pull_request_count": args.pull_request_count,
        "default_branch_contains_verified_commit": containment.returncode == 0,
        "tags_containing_verified_commit": tags,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    write_json(RUN_ROOT / "FRESH_CLONE_REMEDIATION_VERIFICATION.json", result)
    (RUN_ROOT / "FRESH_CLONE_REMEDIATION_VERIFICATION.md").write_text("\n".join([
        "# Fresh-Clone Remediation Verification", "",
        f"Result: `{result['status']}` (`{result['checks_passed']}/{result['checks_total']}` checks)", "",
        f"- Verified pushed remediation evidence commit: `{target}`",
        f"- Branch: `{BRANCH}`",
        f"- Checksum entries: `{result['checksum_entries']}`; failures: `{len(checksum_failures)}`",
        f"- Evidence-manifest entries: `{result['evidence_manifest_entries']}`; failures: `{len(manifest_failures)}`",
        f"- Immutable baseline entries: `{result['baseline_entries']}`; failures: `{len(baseline_failures)}`",
        f"- Package ZIP SHA-256: `{result['package_zip_sha256']}`",
        f"- Open pull requests for branch: `{result['pull_request_count']}`",
        f"- Verified commit contained in default branch: `{str(result['default_branch_contains_verified_commit']).lower()}`",
        f"- Tags containing verified commit: `{len(tags)}`",
        "- Merge, release, and deployment performed by this run: no", "",
        "The fresh clone confirms the integrity and publication of the blocked remediation evidence. It does not convert the failed canary into activation readiness.", "",
    ]), encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": f"{result['checks_passed']}/{result['checks_total']}"}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
