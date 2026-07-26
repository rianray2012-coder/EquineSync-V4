#!/usr/bin/env python3
"""Validate the CGP-006 initiation package.

This validator is documentary and repository-local. It verifies the initiation
package without adopting a guide, activating a gate, or changing product CI.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from cgp_validation import ValidationResult, code_root, read_csv_strict, repo_root_from


BASELINE = "3eb6825091241709f255b8ccf296987fa9b20724"
PR23_BASE = "636b104a8766f08eb1e4b57d1bc840ef217187e9"
PR23_MERGE = "3eb6825091241709f255b8ccf296987fa9b20724"
PACKAGE_REL = Path("initiation/CGP-006")
WAVE_GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
EXPECTED_COUNTS = {"ES-CG-00": 29, "ES-CG-01": 34, "ES-CG-13": 45, "ES-CG-10": 31}
REQUIRED_FILES = (
    "CGP_006_INITIATION_ASSESSMENT.md",
    "CGP_006_PR23_CONFLICT_ASSESSMENT.md",
    "CGP_006_SCOPE_AND_BOUNDARY.md",
    "CGP_006_INPUT_REGISTER.md",
    "CGP_006_OUTPUT_REGISTER.md",
    "CGP_006_FOUNDER_DECISION_REGISTER.md",
    "CGP_006_RISK_FINDING_DEVIATION_REGISTER.csv",
    "CGP_006_VALIDATION_PLAN.md",
    "CGP_006_REPOSITORY_LIFECYCLE_PLAN.md",
    "CGP_006_AUTHORITY_BOUNDARY.md",
    "CGP_006_PACKAGE_MANIFEST.json",
    "CGP_006_CHECKSUMS.sha256",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_output(repo: Path, args: list[str]) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=False)
    if proc.returncode:
        return ""
    return proc.stdout.strip()


def _load_json(path: Path, result: ValidationResult) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_json", "JSON artifact is missing.", path)
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"JSON parsing failed: {exc}", path)
    return {}


def validate_cgp006_initiation(root: Path, required_files: tuple[str, ...] = REQUIRED_FILES) -> ValidationResult:
    result = ValidationResult("cgp006-initiation")
    repo = root.parents[2]
    package_dir = root / PACKAGE_REL
    if not package_dir.exists():
        result.add("missing_cgp006_package", "CGP-006 initiation package directory is missing.", package_dir)
        return result.finalize()

    for name in required_files:
        if not (package_dir / name).exists():
            result.add("missing_cgp006_artifact", "Required CGP-006 artifact is missing.", package_dir / name, name)

    manifest_path = package_dir / "CGP_006_PACKAGE_MANIFEST.json"
    ledger_path = package_dir / "CGP_006_CHECKSUMS.sha256"
    manifest = _load_json(manifest_path, result)
    if manifest:
        if manifest.get("starting_commit") != BASELINE:
            result.add("baseline_mismatch", "Manifest starting commit does not match refreshed baseline.", manifest_path)
        if manifest.get("pr23_conflict_assessment") != "PR23_REVIEWED_NON_CONFLICTING_WITH_CGP_BASELINE":
            result.add("pr23_conflict_not_cleared", "Manifest does not record non-conflicting PR #23 assessment.", manifest_path)
        if manifest.get("reference_corpus_classification") != "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE":
            result.add("reference_corpus_treated_as_normative", "Manifest must keep reference corpus non-normative.", manifest_path)
        if manifest.get("reference_corpus_count") != 2511:
            result.add("reference_corpus_count_mismatch", "Manifest reference corpus count must be 2511.", manifest_path)
        if manifest.get("reference_only_exclusion_count") != 8714:
            result.add("reference_only_count_mismatch", "Manifest reference-only exclusion count must be 8714.", manifest_path)
        if manifest.get("normative_counts") != EXPECTED_COUNTS:
            result.add("normative_count_mismatch", "Manifest normative counts do not match CGP-005 freeze.", manifest_path)
        paths = [item.get("path", "") for item in manifest.get("files", [])]
        if len(paths) != len(set(paths)):
            result.add("duplicate_manifest_path", "Manifest contains duplicate file paths.", manifest_path)
        for rel in paths:
            if not rel.startswith("governance/implementation/code-guides/"):
                result.add("outside_scope_manifest_path", "Manifest path is outside Code Guide scope.", manifest_path, rel)
            elif not (repo / rel).exists():
                result.add("missing_manifest_file", "Manifest path does not resolve.", manifest_path, rel)

    if ledger_path.exists():
        seen: set[str] = set()
        for line_no, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                digest, rel = line.split("  ", 1)
            except ValueError:
                result.add("malformed_checksum_line", "Checksum line must use a two-space separator.", ledger_path, str(line_no))
                continue
            seen.add(rel)
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                result.add("malformed_checksum", "Checksum must be 64 lowercase hex characters.", ledger_path, rel)
                continue
            actual = root / rel
            if not actual.exists():
                result.add("missing_checksum_file", "Checksum references missing file.", ledger_path, rel)
            elif sha256_file(actual) != digest:
                result.add("checksum_mismatch", "Checksum mismatch.", ledger_path, rel)
        if "initiation/CGP-006/CGP_006_CHECKSUMS.sha256" in seen:
            result.add("checksum_self_hash", "Checksum ledger must exclude itself.", ledger_path)
        if "initiation/CGP-006/CGP_006_PACKAGE_MANIFEST.json" in seen:
            result.add("manifest_self_hash", "Manifest must not self-hash inside its own ledger.", ledger_path)

    pr23_text = (package_dir / "CGP_006_PR23_CONFLICT_ASSESSMENT.md").read_text(encoding="utf-8") if (package_dir / "CGP_006_PR23_CONFLICT_ASSESSMENT.md").exists() else ""
    if "PR23_REVIEWED_NON_CONFLICTING_WITH_CGP_BASELINE" not in pr23_text:
        result.add("pr23_conflict_assessment_missing", "PR #23 non-conflict finding is missing.", package_dir / "CGP_006_PR23_CONFLICT_ASSESSMENT.md")
    pr23_files = git_output(repo, ["diff", "--name-only", PR23_BASE, PR23_MERGE]).splitlines()
    if any(path.startswith("governance/implementation/code-guides/") for path in pr23_files):
        result.add("pr23_code_guide_diff", "PR #23 changed Code Guide Program files.", package_dir / "CGP_006_PR23_CONFLICT_ASSESSMENT.md")

    _, tracker_rows = read_csv_strict(root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv", result)
    tracker = {row.get("record_id", ""): row for row in tracker_rows}
    cgp005 = tracker.get("CGP-005", {})
    cgp006 = tracker.get("CGP-006", {})
    if cgp005.get("prompt_status") != "ACCEPTED" or cgp005.get("accession_state") != "REPOSITORY_ACCESSIONED":
        result.add("cgp005_state_mismatch", "CGP-005 must remain accepted and repository-accessioned.", root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv", "CGP-005")
    if cgp006.get("prompt_status") != "NOT_ISSUED":
        result.add("cgp006_issued_without_authority", "CGP-006 substantive drafting must remain NOT_ISSUED.", root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv", "CGP-006")
    for guide in WAVE_GUIDES:
        row = tracker.get(guide, {})
        if row.get("maturity_state") != "SOURCE_FROZEN":
            result.add("wave1_maturity_changed", "Wave 1 guide must remain SOURCE_FROZEN.", root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv", guide)
        if row.get("adoption_state") != "NOT_ADOPTED":
            result.add("guide_adopted_without_authority", "Wave 1 guide must remain NOT_ADOPTED.", root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv", guide)
        if row.get("work_status") != "SOURCE_FROZEN":
            result.add("wave1_work_status_changed", "Wave 1 guide work status must remain SOURCE_FROZEN.", root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv", guide)

    ref_manifest = _load_json(root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json", result)
    if ref_manifest.get("classification") != "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE":
        result.add("reference_corpus_treated_as_normative", "CGP-005 reference corpus must remain non-normative.", root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json")
    if ref_manifest.get("source_count") != 2511:
        result.add("reference_corpus_count_mismatch", "CGP-005 reference corpus count must remain 2511.", root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json")
    _, crosswalk_rows = read_csv_strict(root / "source-freeze" / "WAVE_1_SOURCE_FREEZE_CROSSWALK.csv", result)
    if len(crosswalk_rows) != 139:
        result.add("normative_crosswalk_count_mismatch", "Normative crosswalk row count must remain 139.", root / "source-freeze" / "WAVE_1_SOURCE_FREEZE_CROSSWALK.csv")
    for guide, expected in EXPECTED_COUNTS.items():
        _, rows = read_csv_strict(root / "guides" / guide / "source-freeze" / f"{guide}_SOURCE_FREEZE_REGISTER.csv", result)
        if len(rows) != expected:
            result.add("guide_normative_count_mismatch", "Guide normative source row count changed.", root / "guides" / guide / "source-freeze" / f"{guide}_SOURCE_FREEZE_REGISTER.csv", guide)

    _, decision_rows = read_csv_strict(package_dir / "CGP_006_RISK_FINDING_DEVIATION_REGISTER.csv", result)
    result.summary["risk_rows_checked"] = len(decision_rows)
    decision_text = (package_dir / "CGP_006_FOUNDER_DECISION_REGISTER.md").read_text(encoding="utf-8") if (package_dir / "CGP_006_FOUNDER_DECISION_REGISTER.md").exists() else ""
    for decision_id in [f"CGP006-D-{i:04d}" for i in range(1, 7)]:
        if decision_id not in decision_text:
            result.add("missing_founder_decision", "Expected CGP-006 Founder decision ID is missing.", package_dir / "CGP_006_FOUNDER_DECISION_REGISTER.md", decision_id)
    if decision_text.count("PENDING_FOUNDER_REVIEW") < 6:
        result.add("founder_decision_status_missing", "Founder decisions must remain pending review.", package_dir / "CGP_006_FOUNDER_DECISION_REGISTER.md")

    result.summary.update(
        {
            "required_files": len(required_files),
            "manifest_files": len(manifest.get("files", [])) if manifest else 0,
            "ledger_entries": len(seen) if ledger_path.exists() else 0,
            "pr23_files_reviewed": len(pr23_files),
            "normative_crosswalk_rows": len(crosswalk_rows) if "crosswalk_rows" in locals() else 0,
        }
    )
    return result.finalize()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="Path to governance/implementation/code-guides")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()
    root = args.root.resolve() if args.root else code_root(repo_root_from(Path.cwd()))
    result = validate_cgp006_initiation(root)
    payload = result.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{payload['validator']}: {payload['status']}")
        for issue in payload["issues"]:
            print(f"- {issue['severity']} {issue['code']} {issue['record_id']} {issue['path']}: {issue['message']}")
        print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return result.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
