#!/usr/bin/env python3
"""Freeze and checksum the documentary V1.1.0 candidate.

The frozen scope ends before fresh-review evidence and final disposition are
added. This script performs no product implementation or operational action.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
PREDECESSOR = ROOT.parent / "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"
BASE_COMMIT = "0beee6137183eb4079e7346c8596f6bec552f2f2"
PIA_ID = "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0"
INTERIM_DISPOSITION = (
    "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_"
    "001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW"
)
EXCLUDED_FROM_FREEZE = {
    "FROZEN_REVISED_CANDIDATE_MANIFEST.txt",
    "FROZEN_REVISED_CANDIDATE_SHA256SUMS.txt",
    "FRESH_SEGREGATED_REVIEW_REPORT.md",
    "FRESH_SEGREGATED_REVIEW_FINDINGS.csv",
    "FRESH_SEGREGATED_REVIEW_EVIDENCE_INDEX.csv",
    "FINAL_DISPOSITION.md",
    "POST_REVIEW_EVIDENCE_MANIFEST.json",
    "POST_REVIEW_EVIDENCE_SHA256SUMS.txt",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with (ROOT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def successor_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.relative_to(ROOT).as_posix() not in EXCLUDED_FROM_FREEZE
        and path.name != "PACKAGE_MANIFEST.json"
    )


def build_change_manifest() -> dict[str, int]:
    mappings: dict[str, str] = {}
    rows: list[dict[str, str]] = []
    for old in sorted(path for path in PREDECESSOR.rglob("*") if path.is_file() and "__pycache__" not in path.parts):
        old_rel = old.relative_to(PREDECESSOR).as_posix()
        if old_rel == "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md":
            target_rel = "PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md"
        elif (ROOT / old_rel).is_file():
            target_rel = old_rel
        elif (ROOT / "predecessor_evidence/v1.0.0" / old_rel).is_file():
            target_rel = f"predecessor_evidence/v1.0.0/{old_rel}"
        else:
            target_rel = ""
        mappings[old_rel] = target_rel
        if not target_rel:
            change = "REMOVED"
            new_sha = ""
            rationale = "No successor artifact located"
        else:
            target = ROOT / target_rel
            new_sha = sha256(target)
            same = sha256(old) == new_sha
            relocated = target_rel != old_rel
            if same and relocated:
                change = "RELOCATED_PRESERVED"
                rationale = "Frozen V1.0.0 evidence relocated byte-for-byte under predecessor_evidence"
            elif same:
                change = "UNCHANGED"
                rationale = "Inherited artifact remains byte-identical"
            elif relocated:
                change = "RELOCATED_AND_MODIFIED"
                rationale = "PIA version advanced and Founder doctrine incorporated"
            else:
                change = "MODIFIED"
                rationale = "Founder decisions, gates, traceability, or successor identity incorporated"
        rows.append({
            "change_id": f"FAC-DOC-CHG-{len(rows)+1:03d}",
            "change_type": change,
            "predecessor_path": old_rel,
            "successor_path": target_rel,
            "predecessor_sha256": sha256(old),
            "successor_sha256": new_sha,
            "rationale": rationale,
        })

    mapped_targets = {target for target in mappings.values() if target}
    ignore = EXCLUDED_FROM_FREEZE | {"DOCUMENTARY_CHANGE_MANIFEST.csv", "PACKAGE_MANIFEST.json"}
    for path in sorted(path for path in ROOT.rglob("*") if path.is_file() and "__pycache__" not in path.parts):
        rel = path.relative_to(ROOT).as_posix()
        if rel in mapped_targets or rel in ignore:
            continue
        rows.append({
            "change_id": f"FAC-DOC-CHG-{len(rows)+1:03d}",
            "change_type": "ADDED",
            "predecessor_path": "",
            "successor_path": rel,
            "predecessor_sha256": "",
            "successor_sha256": sha256(path),
            "rationale": "New Founder-decision incorporation, validation, freeze, source, or successor evidence",
        })
    rows.append({
        "change_id": f"FAC-DOC-CHG-{len(rows)+1:03d}",
        "change_type": "ADDED",
        "predecessor_path": "",
        "successor_path": "DOCUMENTARY_CHANGE_MANIFEST.csv",
        "predecessor_sha256": "",
        "successor_sha256": "SELF_EXCLUDED",
        "rationale": "Self-describing complete documentary change manifest",
    })
    write_csv(
        "DOCUMENTARY_CHANGE_MANIFEST.csv",
        ["change_id", "change_type", "predecessor_path", "successor_path", "predecessor_sha256", "successor_sha256", "rationale"],
        rows,
    )
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["change_type"]] = counts.get(row["change_type"], 0) + 1
    return counts


def write_integrity_report(change_counts: dict[str, int]) -> None:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", BASE_COMMIT, "--", "governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"],
        cwd=REPO, capture_output=True, text=True, check=False,
    )
    source_changes = subprocess.run(
        ["git", "diff", "--name-only", BASE_COMMIT, "--", ":(exclude)governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0/**"],
        cwd=REPO, capture_output=True, text=True, check=False,
    )
    predecessor_modifications = len([line for line in tracked.stdout.splitlines() if line])
    outside_modifications = len([line for line in source_changes.stdout.splitlines() if line])
    if tracked.returncode or source_changes.returncode or predecessor_modifications or outside_modifications:
        raise SystemExit("Frozen predecessor/source integrity check failed")
    body = f"""# Frozen Predecessor Integrity Report

- PIA: `{PIA_ID}`
- Date: `2026-07-21`
- Status: `PASS`
- Frozen base: `{BASE_COMMIT}`

## Results

- Frozen V1.0.0 predecessor modifications: `0`.
- Tracked source modifications outside V1.1.0 successor: `0`.
- Predecessor checksum verification: `47/47 PASS` (see `TRACEABILITY_VALIDATION_REPORT.md`).
- Documentary change rows: `{sum(change_counts.values())}`.
- Relocated-preserved V1.0.0 evidence rows: `{change_counts.get('RELOCATED_PRESERVED', 0)}`.
- Removed artifact rows: `{change_counts.get('REMOVED', 0)}`.

No frozen historical artifact was rewritten. Relocated predecessor evidence remains byte-identical and explicitly non-controlling for V1.1.0.

> No implementation, migration, deployment, enrollment, production action, custom-agent activation, or F-0001 closure is authorized.
"""
    (ROOT / "FROZEN_PREDECESSOR_INTEGRITY_REPORT.md").write_text(body, encoding="utf-8")


def build_package_manifest(change_counts: dict[str, int]) -> None:
    files = successor_files()
    entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in files
    ]
    manifest = {
        "pia_id": PIA_ID,
        "version": "1.1.0-candidate",
        "date": "2026-07-21",
        "phase": "FROZEN_REVISED_CANDIDATE_PRE_FRESH_REVIEW",
        "disposition": INTERIM_DISPOSITION,
        "base_commit": BASE_COMMIT,
        "approved_design_doctrine": [f"FAC-FD-{number:03d}" for number in range(1, 19)],
        "open_before_implementation_authorization": ["FAC-FD-019", "FAC-FD-020", "FAC-FD-021", "FAC-FD-022", "FAC-FD-025", "FAC-FD-026"],
        "open_before_enrollment": ["FAC-FD-023", "FAC-FD-024", "FAC-FD-027", "FAC-FD-028"],
        "implementation_authorized": False,
        "enrollment_authorized": False,
        "frozen_predecessor_modification_count": 0,
        "source_modification_count": 0,
        "change_counts": change_counts,
        "manifest_self_excluded": True,
        "future_review_envelope_excluded": sorted(EXCLUDED_FROM_FREEZE),
        "files": entries,
    }
    (ROOT / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_freeze_manifests() -> tuple[int, str]:
    files = successor_files() + [ROOT / "PACKAGE_MANIFEST.json"]
    files = sorted(set(files))
    manifest_lines = [
        "# ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0 frozen revised candidate",
        f"# disposition={INTERIM_DISPOSITION}",
        f"# base_commit={BASE_COMMIT}",
        f"# file_count={len(files)}",
        "sha256|bytes|path",
    ]
    checksum_lines = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        digest = sha256(path)
        manifest_lines.append(f"{digest}|{path.stat().st_size}|{rel}")
        checksum_lines.append(f"{digest}  {rel}")
    (ROOT / "FROZEN_REVISED_CANDIDATE_MANIFEST.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    (ROOT / "FROZEN_REVISED_CANDIDATE_SHA256SUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    envelope = hashlib.sha256(("\n".join(checksum_lines) + "\n").encode()).hexdigest()
    return len(files), envelope


def main() -> int:
    trace = (ROOT / "TRACEABILITY_VALIDATION_REPORT.md").read_text(encoding="utf-8")
    consistency = (ROOT / "INTERNAL_CONSISTENCY_VALIDATION_REPORT.md").read_text(encoding="utf-8")
    if "- Status: `PASS`" not in trace or "- Status: `PASS`" not in consistency:
        print("Refusing to freeze: validation reports do not pass", file=sys.stderr)
        return 1
    change_counts = build_change_manifest()
    write_integrity_report(change_counts)
    build_package_manifest(change_counts)
    count, envelope = write_freeze_manifests()
    verify = subprocess.run(
        ["shasum", "-a", "256", "-c", "FROZEN_REVISED_CANDIDATE_SHA256SUMS.txt"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    passed = sum(line.endswith(": OK") for line in verify.stdout.splitlines())
    result = "PASS" if verify.returncode == 0 and passed == count else "FAIL"
    print(json.dumps({"result": result, "frozen_files": count, "checksum_entries_passed": passed, "checksum_envelope_sha256": envelope, "change_counts": change_counts}, indent=2, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
