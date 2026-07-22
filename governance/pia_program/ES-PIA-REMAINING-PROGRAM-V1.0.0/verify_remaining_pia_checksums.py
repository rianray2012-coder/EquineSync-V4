#!/usr/bin/env python3
"""Verify the frozen Remaining PIA SHA-256 ledger in parallel."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "REMAINING_PIA_CHECKSUMS.sha256"
EXPECTED_TOTAL_FILES = 90
EXPECTED_LEDGER_ENTRIES = 89


def main() -> int:
    entries: list[tuple[str, str]] = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        entries.append((digest, relative))

    actual_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".DS_Store" not in path.parts
        and "__pycache__" not in path.parts
    )
    covered_files = sorted(relative for _, relative in entries)
    expected_covered_files = sorted(
        relative for relative in actual_files if relative != LEDGER.name
    )
    structural_failures: list[str] = []
    if len(actual_files) != EXPECTED_TOTAL_FILES:
        structural_failures.append(
            f"total package files: expected {EXPECTED_TOTAL_FILES}, found {len(actual_files)}"
        )
    if len(entries) != EXPECTED_LEDGER_ENTRIES:
        structural_failures.append(
            f"ledger entries: expected {EXPECTED_LEDGER_ENTRIES}, found {len(entries)}"
        )
    if len(covered_files) != len(set(covered_files)):
        structural_failures.append("checksum ledger contains duplicate filenames")
    if LEDGER.name in covered_files:
        structural_failures.append(f"checksum ledger must self-exclude {LEDGER.name}")
    if covered_files != expected_covered_files:
        structural_failures.append(
            "checksum ledger filenames do not equal all non-self package files"
        )

    def verify(entry: tuple[str, str]) -> tuple[str, bool, str]:
        expected, relative = entry
        path = ROOT / relative
        if not path.is_file():
            return relative, False, "MISSING"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        return relative, actual == expected, actual

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(verify, entries))

    failures = [result for result in results if not result[1]]
    print(f"total_package_files={len(actual_files)}")
    print(f"ledger_entries={len(entries)}")
    print(f"checksum_ledger_self_excluded={LEDGER.name}")
    print("checksum_ledger_self_exclusion_intentional=true")
    print(f"verified={len(entries) - len(failures)}")
    for failure in structural_failures:
        print(f"FAIL {failure}")
    for relative, _, actual in failures:
        print(f"FAIL {relative} actual={actual}")
    passed = not failures and not structural_failures
    print("RESULT:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
