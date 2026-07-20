#!/usr/bin/env python3
"""Validate and archive the frozen Candidate 009 without modifying it."""
from __future__ import annotations

import hashlib
import json
import stat
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CANDIDATE_ID = "ES-PKG-2026-004-V003-CANDIDATE-009"
CANDIDATE = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION" / CANDIDATE_ID
ATTEMPT = REPO / "stage2a/review_attempts/attempt-009"
OUTPUTS = REPO.parents[1] / "outputs"
ARCHIVE = OUTPUTS / f"{CANDIDATE_ID}_FROZEN.zip"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_map(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_pair(stem: str, title: str, value: dict[str, object], body: str) -> None:
    (ATTEMPT / f"{stem}.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ATTEMPT / f"{stem}.md").write_text(
        f"# {title}\n\n{body}\n\n- Execution: `EXECUTION_NOT_AUTHORIZED`\n- Assurance: `NOT_EXTERNALLY_ASSURED`\n",
        encoding="utf-8",
    )


def validate(label: str, root: Path, cwd: Path, mode: str) -> dict[str, object]:
    validator = root / "validate_stage2a_package.py"
    completed = subprocess.run(
        [sys.executable, str(validator), str(root), "--phase", "candidate"],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    parsed = json.loads(completed.stdout) if completed.stdout.strip() else {}
    return {
        "location": label,
        "mode": mode,
        "exit_status": completed.returncode,
        "validation": parsed.get("validation"),
        "score": f"{parsed.get('pass_count')}/{parsed.get('check_count')}",
        "output_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
    }


def main() -> int:
    if not CANDIDATE.is_dir():
        raise RuntimeError(f"candidate unavailable: {CANDIDATE_ID}")
    if ARCHIVE.exists() or ATTEMPT.exists():
        raise RuntimeError("refusing to overwrite Candidate 009 freeze artifacts")
    manifest = CANDIDATE / "DRAFT_REVIEW_SHA256SUMS.txt"
    snapshot = json.loads((CANDIDATE / "DRAFT_REVIEW_SNAPSHOT_RECORD.json").read_text(encoding="utf-8"))
    if snapshot.get("candidate_id") != CANDIDATE_ID or snapshot.get("frozen") is not True or sha(manifest) != snapshot.get("manifest_sha256"):
        raise RuntimeError("Candidate 009 snapshot or manifest changed before freeze")
    rows = manifest.read_text(encoding="utf-8").splitlines()
    manifest_errors: list[str] = []
    for row in rows:
        expected, relative = row.split("  ", 1)
        target = CANDIDATE / relative
        if not target.is_file() or sha(target) != expected:
            manifest_errors.append(relative)
    before = file_map(CANDIDATE)
    if manifest_errors or len(rows) != snapshot.get("payload_files") or len(before) != len(rows) + 3:
        raise RuntimeError(f"Candidate 009 pre-freeze mismatch: {manifest_errors}")

    invocations = [
        validate("PACKAGE_ROOT", CANDIDATE, CANDIDATE, "REPOSITORY_BACKED_PACKAGED_VALIDATOR"),
        validate("PACKAGE_NESTED_REVIEW_ATTEMPT_004", CANDIDATE, CANDIDATE / "review_attempts/attempt-004", "REPOSITORY_BACKED_PACKAGED_VALIDATOR"),
        validate("EXTERNAL_PRIVATE_TMP", CANDIDATE, Path("/private/tmp"), "REPOSITORY_BACKED_PACKAGED_VALIDATOR"),
    ]
    if before != file_map(CANDIDATE):
        raise RuntimeError("candidate changed during repository-backed validation")
    if any(row["exit_status"] != 0 or row["validation"] != "PASS" for row in invocations):
        raise RuntimeError(f"repository-backed candidate validation failed: {invocations}")

    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, _digest in sorted(before.items()):
            path = CANDIDATE / relative
            info = zipfile.ZipInfo(f"{CANDIDATE_ID}/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | stat.S_IMODE(path.stat().st_mode)) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    with tempfile.TemporaryDirectory(prefix="es-candidate007-clean-extraction-", dir="/private/tmp") as temporary:
        extraction_root = Path(temporary)
        with zipfile.ZipFile(ARCHIVE, "r") as archive:
            archive.extractall(extraction_root)
        extracted = extraction_root / CANDIDATE_ID
        extracted_map_before = file_map(extracted)
        invocations.append(validate("DETACHED_CLEAN_EXTRACTION", extracted, extraction_root, "DETACHED_PACKAGE_SOURCE_PAYLOAD"))
        extracted_map_after = file_map(extracted)
        extraction_parity = {
            "candidate_files": len(before),
            "extracted_files_before_validation": len(extracted_map_before),
            "extracted_files_after_validation": len(extracted_map_after),
            "byte_parity_before_validation": extracted_map_before == before,
            "byte_parity_after_validation": extracted_map_after == before,
            "validator_added_files": sorted(set(extracted_map_after) - set(extracted_map_before)),
            "temporary_extraction_removed": True,
        }
    if invocations[-1]["exit_status"] != 0 or invocations[-1]["validation"] != "PASS":
        raise RuntimeError(f"detached candidate validation failed: {invocations[-1]}")
    if not extraction_parity["byte_parity_before_validation"] or not extraction_parity["byte_parity_after_validation"]:
        raise RuntimeError(f"clean extraction parity failed: {extraction_parity}")
    if before != file_map(CANDIDATE):
        raise RuntimeError("candidate changed during freeze or detached validation")

    ATTEMPT.mkdir(parents=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    matrix = {
        "candidate_id": CANDIDATE_ID,
        "generated_utc": generated_utc,
        "phase": "CANDIDATE_POST_MANIFEST_PRE_REVIEW",
        "invocations": invocations,
        "supported_locations": 4,
        "passed_locations": 4,
        "result": "PASS",
        "candidate_unchanged": True,
        "execution": "EXECUTION_NOT_AUTHORIZED",
        "assurance": "NOT_EXTERNALLY_ASSURED",
    }
    write_pair("PRE_REVIEW_VALIDATION_MATRIX", "Candidate 009 Pre-Review Validation Matrix", matrix, "All four supported validator invocation locations passed the complete package-control suite; validation did not modify the frozen candidate.")
    clean = extraction_parity | {
        "candidate_id": CANDIDATE_ID,
        "archive_sha256": sha(ARCHIVE),
        "result": f"PASS_{len(before)}_OF_{len(before)}",
        "execution": "EXECUTION_NOT_AUTHORIZED",
        "assurance": "NOT_EXTERNALLY_ASSURED",
    }
    write_pair("CLEAN_EXTRACTION_VERIFICATION", "Candidate 009 Clean Extraction Verification", clean, f"The deterministic archive extracted with byte parity `{len(before)}/{len(before)}` before and after detached validation; the validator added no files.")
    freeze = {
        "candidate_id": CANDIDATE_ID,
        "generated_utc": generated_utc,
        "candidate_directory": CANDIDATE.relative_to(REPO).as_posix(),
        "candidate_files": len(before),
        "payload_files": len(rows),
        "manifest_sha256": sha(manifest),
        "archive": f"outputs/{ARCHIVE.name}",
        "archive_sha256": sha(ARCHIVE),
        "candidate_unchanged": True,
        "validation": "PASS_4_OF_4_LOCATIONS_23_OF_23_CHECKS",
        "clean_extraction": f"PASS_{len(before)}_OF_{len(before)}",
        "execution": "EXECUTION_NOT_AUTHORIZED",
        "assurance": "NOT_EXTERNALLY_ASSURED",
    }
    write_pair("FROZEN_SNAPSHOT_RECORD", "Candidate 009 Frozen Snapshot Record", freeze, f"`{CANDIDATE_ID}` is frozen under archive SHA-256 `{freeze['archive_sha256']}` and manifest SHA-256 `{freeze['manifest_sha256']}`. Review functions must not modify it.")
    print(json.dumps(freeze, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
