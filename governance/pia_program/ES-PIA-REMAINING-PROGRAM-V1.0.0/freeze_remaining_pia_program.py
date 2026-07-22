#!/usr/bin/env python3
"""Generate the deterministic program file manifest and SHA-256 ledger."""
from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILE_MANIFEST = ROOT / "REMAINING_PIA_FILE_MANIFEST.txt"
CHECKSUMS = ROOT / "REMAINING_PIA_CHECKSUMS.sha256"
EXPECTED_TOTAL_FILES = 119
EXPECTED_CHECKSUMMED_FILES = 118


def included_files() -> list[Path]:
    paths = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".DS_Store" not in path.parts
        and "__pycache__" not in path.parts
    ]
    for generated in (FILE_MANIFEST, CHECKSUMS):
        if generated not in paths:
            paths.append(generated)
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> int:
    paths = included_files()
    if len(paths) != EXPECTED_TOTAL_FILES:
        raise RuntimeError(
            f"expected {EXPECTED_TOTAL_FILES} total package files, found {len(paths)}"
        )
    if CHECKSUMS not in paths:
        raise RuntimeError(f"missing checksum ledger: {CHECKSUMS.name}")
    FILE_MANIFEST.write_text(
        "\n".join(path.relative_to(ROOT).as_posix() for path in paths) + "\n",
        encoding="utf-8",
    )

    checksum_paths = [path for path in paths if path != CHECKSUMS]
    if len(checksum_paths) != EXPECTED_CHECKSUMMED_FILES:
        raise RuntimeError(
            f"expected {EXPECTED_CHECKSUMMED_FILES} checksum-covered files, "
            f"found {len(checksum_paths)}"
        )

    def checksum_line(path: Path) -> str:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return f"{digest}  {path.relative_to(ROOT).as_posix()}"

    with ThreadPoolExecutor(max_workers=16) as executor:
        lines = list(executor.map(checksum_line, checksum_paths))
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"total_package_files={len(paths)}")
    print(f"checksum_covered_files={len(checksum_paths)}")
    print(f"checksum_ledger_self_excluded={CHECKSUMS.name}")
    print("checksum_ledger_self_exclusion_intentional=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
