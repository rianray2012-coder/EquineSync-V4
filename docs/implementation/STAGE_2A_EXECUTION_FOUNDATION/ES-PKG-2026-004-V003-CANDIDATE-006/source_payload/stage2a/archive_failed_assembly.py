#!/usr/bin/env python3
"""Preserve a pre-freeze failed candidate without modifying its directory."""
from __future__ import annotations

import hashlib
import json
import stat
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CANDIDATE_ID = "ES-PKG-2026-004-V003-CANDIDATE-005"
CANDIDATE = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION" / CANDIDATE_ID
EVIDENCE = REPO / "stage2a/evidence/failed_attempts"
OUTPUTS = REPO.parents[1] / "outputs"
MANIFEST = EVIDENCE / "CANDIDATE_005_ASSEMBLY_FAILED_SHA256SUMS.txt"
REPORT_JSON = EVIDENCE / "CANDIDATE_005_ASSEMBLY_FAILED.json"
REPORT_MD = EVIDENCE / "CANDIDATE_005_ASSEMBLY_FAILED.md"
ARCHIVE = OUTPUTS / f"{CANDIDATE_ID}_ASSEMBLY_FAILED.zip"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not CANDIDATE.is_dir():
        raise RuntimeError(f"failed candidate unavailable: {CANDIDATE_ID}")
    for output in (MANIFEST, REPORT_JSON, REPORT_MD, ARCHIVE):
        if output.exists():
            raise RuntimeError(f"refusing to overwrite preservation artifact: {output.name}")

    files = sorted(path for path in CANDIDATE.rglob("*") if path.is_file())
    rows = [f"{sha(path)}  {path.relative_to(CANDIDATE).as_posix()}" for path in files]
    MANIFEST.write_text("\n".join(rows) + "\n", encoding="utf-8")

    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = Path(CANDIDATE_ID) / path.relative_to(CANDIDATE)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = stat.S_IMODE(path.stat().st_mode)
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    provenance = json.loads((CANDIDATE / "CORRECTED_CANDIDATE_PROVENANCE.json").read_text(encoding="utf-8"))
    report = {
        "candidate_id": CANDIDATE_ID,
        "classification": "PRE_FREEZE_ASSEMBLY_VALIDATION_FAILED",
        "preserved_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_directory": CANDIDATE.relative_to(REPO).as_posix(),
        "candidate_directory_modified_by_preservation": False,
        "file_count": len(files),
        "manifest": MANIFEST.relative_to(REPO).as_posix(),
        "manifest_sha256": sha(MANIFEST),
        "archive": f"outputs/{ARCHIVE.name}",
        "archive_sha256": sha(ARCHIVE),
        "validated_implementation_commit": provenance["validated_implementation_commit"],
        "packaging_commit": provenance["packaging_commit"],
        "validator_result": {
            "repository_backed_locations_passed": 3,
            "repository_backed_locations_required": 3,
            "detached_clean_copy_score": "22/23",
            "failed_check": "MV-011-source-register",
            "cause": "dynamic detached source-module imports created two __pycache__ files inside source_payload",
        },
        "execution": "EXECUTION_NOT_AUTHORIZED",
        "assurance": "NOT_EXTERNALLY_ASSURED",
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "# Candidate 005 Assembly Failure Preservation\n\n"
        f"`{CANDIDATE_ID}` is preserved as a distinct pre-freeze failed assembly. Its `{len(files)}` files "
        "were not modified during preservation. Repository-backed validation passed all three supported "
        "locations, but detached clean-copy validation scored `22/23` because dynamic imports created two "
        "bytecode-cache files inside `source_payload`, causing `MV-011-source-register` to fail closed.\n\n"
        f"- Manifest SHA-256: `{report['manifest_sha256']}`\n"
        f"- Archive SHA-256: `{report['archive_sha256']}`\n"
        "- Execution: `EXECUTION_NOT_AUTHORIZED`\n"
        "- Assurance: `NOT_EXTERNALLY_ASSURED`\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
