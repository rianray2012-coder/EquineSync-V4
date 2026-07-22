#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGE_MANIFEST = ROOT / "MODE_B_CHANGE_MANIFEST.txt"
FILE_MANIFEST = ROOT / "MODE_B_FILE_MANIFEST.csv"
CHECKSUMS = ROOT / "MODE_B_CHECKSUMS.sha256"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_excluding(*excluded: Path) -> list[Path]:
    excluded_set = {path.resolve() for path in excluded}
    return [
        path
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.resolve() not in excluded_set and "__pycache__" not in path.parts
    ]


def main() -> None:
    initial_files = files_excluding(CHANGE_MANIFEST, FILE_MANIFEST, CHECKSUMS)
    change_lines = [
        "EQUINESYNC PHASE 1 PILOT A MODE B ATTEMPT 04 CHANGE MANIFEST",
        "",
        "Additive scope: new attempt-04 evidence only.",
        "Attempt 01 modified: no",
        "Attempt 02 modified: no",
        "Default branch modified: no",
        "Pull request created: no",
        "Phase 2 activity: no",
        "",
        "FILES",
    ]
    change_lines.extend(path.relative_to(ROOT).as_posix() for path in initial_files)
    change_lines.extend([
        CHANGE_MANIFEST.relative_to(ROOT).as_posix(),
        FILE_MANIFEST.relative_to(ROOT).as_posix(),
        CHECKSUMS.relative_to(ROOT).as_posix(),
    ])
    CHANGE_MANIFEST.write_text("\n".join(change_lines) + "\n", encoding="utf-8")

    manifest_files = files_excluding(FILE_MANIFEST, CHECKSUMS)
    with FILE_MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["path", "size_bytes", "sha256"])
        for path in manifest_files:
            writer.writerow([path.relative_to(ROOT).as_posix(), path.stat().st_size, sha256(path)])

    checksum_files = files_excluding(CHECKSUMS)
    CHECKSUMS.write_text(
        "".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in checksum_files),
        encoding="utf-8",
    )
    print(f"change_manifest_files={len(initial_files)}")
    print(f"file_manifest_rows={len(manifest_files)}")
    print(f"checksum_entries={len(checksum_files)}")


if __name__ == "__main__":
    main()
