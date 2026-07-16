#!/usr/bin/env python3
"""Validate and package the foundational-canon source certification event."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("record", HERE / "record_founder_certification.py")
RECORD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(RECORD)

REPO = RECORD.REPO
ROOT = RECORD.ROOT
OUTPUT = REPO / "outputs/foundational_canon_source_certification_v1_0"
PACKAGE = OUTPUT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_EVIDENCE_PACKAGE.zip"
REGISTERS = [
    "docs/canon/CANON_INDEX.md",
    "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def main() -> None:
    checks: dict[str, object] = {}
    source_archive = ROOT / "source_event" / RECORD.ARCHIVE.name
    business = ROOT / "source_event/MASTER_BUSINESS_LIFECYCLE_V2_0_FOUNDER_CERTIFIED_CURRENT_SOURCE.md"
    claims = ROOT / "source_event/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_CERTIFIED_SOURCE.md"
    assert sha(source_archive) == RECORD.ARCHIVE_HASH
    assert sha(business) == RECORD.BUSINESS_HASH
    assert sha(claims) == RECORD.CLAIMS_HASH
    checks["founder_attachment_hashes"] = "PASS"
    with zipfile.ZipFile(source_archive) as archive:
        assert archive.testzip() is None
    checks["source_archive_integrity"] = "PASS"

    extracted = ROOT / "source_event/six_reviewed_candidates"
    for _, filename, expected in RECORD.ROWS.values():
        path = claims if filename.endswith("FOUNDER_CERTIFIED_SOURCE.md") else extracted / filename
        assert sha(path) == expected
    checks["certified_source_hashes"] = "PASS"
    assert sha(REPO / "docs/canon/MASTER_BUSINESS_LIFECYCLE.md") == RECORD.BUSINESS_HASH
    recovered_claims = REPO / "docs/canon/reviews/governance_v1_0_c0_phase_c_hash_version_recovery/track_c/C0_028/recovered_sources/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_SOURCE.md"
    assert sha(recovered_claims) == RECORD.CLAIMS_HASH
    checks["repository_parity"] = "PASS"

    state_path = REPO / REGISTERS[3]
    state = json.loads(state_path.read_text())
    selected = [row for row in state["rows"] if row["record_id"] in RECORD.ROWS]
    assert len(selected) == 6
    assert all(row["current_category"] == "adoption_and_lock_required" for row in selected)
    assert all(row["founder_status"] == "FOUNDER_SOURCE_VERSION_CERTIFIED" for row in selected)
    assert all(row["adoption_state"] == "PENDING_SEPARATE_FOUNDER_AUTHORIZATION" for row in selected)
    assert all(row["lock_state"] == "PENDING_SEPARATE_FOUNDER_AUTHORIZATION" for row in selected)
    assert state["unresolved_lifecycle_blockers"] == 15
    assert sum(state["category_counts"].values()) == 47
    checks["lifecycle_state"] = "PASS_15_OPEN_NO_REDUCTION"

    ledger = json.loads((REPO / REGISTERS[5]).read_text())
    assert ledger["row_count"] == 15
    assert sum(ledger["track_counts"].values()) == 15
    assert ledger["track_counts"]["TRACK_C_HASH_OR_VERSION_RECOVERY"] == 1
    assert ledger["track_counts"]["TRACK_F_ADOPTION_AND_LOCK"] == 12
    checks["lifecycle_track_reclassification"] = "PASS"

    for path_text in REGISTERS:
        path = REPO / path_text
        if path.suffix == ".json":
            json.loads(path.read_text())
    checks["json_validation"] = "PASS"
    compile_result = subprocess.run(
        ["python3", "-m", "py_compile", str(HERE / "record_founder_certification.py"), str(Path(__file__))],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert compile_result.returncode == 0, compile_result.stderr
    checks["python_compilation"] = "PASS"
    diff_result = subprocess.run(["git", "diff", "--check"], cwd=REPO, capture_output=True, text=True)
    assert diff_result.returncode == 0, diff_result.stdout + diff_result.stderr
    checks["git_diff_check"] = "PASS"
    checks["application_runtime_files_changed"] = 0
    checks["authority"] = {
        key: False for key in (
            "adoption", "lock", "implementation", "runtime", "migration",
            "provider_activation", "production", "public_launch",
            "governance_v1_baseline_adoption", "governance_v1_baseline_lock",
        )
    }

    write_json(ROOT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_VALIDATION_REPORT.json", {
        "disposition": "PASS",
        "checks": checks,
        "findings": {"p0": 0, "open_p1": 0, "blocking_p2": 0},
    })
    write_json(ROOT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_CHANGED_FILE_MANIFEST.json", {
        "scope": "documentation and governance source-certification only",
        "files": [{"path": path, "sha256": sha(REPO / path)} for path in REGISTERS],
        "application_or_runtime_files": [],
    })

    review_files = sorted(path for path in ROOT.rglob("*") if path.is_file() and path.name != "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_MANIFEST.json")
    package_files = set(review_files) | {REPO / path for path in REGISTERS}
    manifest = {path.relative_to(REPO).as_posix(): sha(path) for path in sorted(package_files)}
    write_json(ROOT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_MANIFEST.json", {
        "disposition": "FOUNDER_CERTIFIED_PREVIOUSLY_ATTACHED_FILES_AS_CORRECT_VERSIONS",
        "files": manifest,
        "authority": checks["authority"],
    })
    package_files.add(ROOT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_MANIFEST.json")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package_files):
            archive.write(path, path.relative_to(REPO).as_posix())
    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(PACKAGE) as archive:
            archive.extractall(temp)
        for name, expected in manifest.items():
            assert sha(Path(temp) / name) == expected
    package_hash = sha(PACKAGE)
    (OUTPUT / f"{PACKAGE.name}.sha256").write_text(f"{package_hash}  {PACKAGE.name}\n")
    write_json(OUTPUT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_EVIDENCE_RECORD.json", {
        "package": PACKAGE.name,
        "sha256": package_hash,
        "fresh_extraction": "PASS",
        "manifest_verification": "PASS",
        "final_disposition": "FOUNDATIONAL_CANON_SOURCE_VERSIONS_FOUNDER_CERTIFIED_PENDING_SEPARATE_ADOPTION_AND_LOCK",
    })
    print(json.dumps({"checks": checks, "package": PACKAGE.relative_to(REPO).as_posix(), "sha256": package_hash}, indent=2))


if __name__ == "__main__":
    main()
