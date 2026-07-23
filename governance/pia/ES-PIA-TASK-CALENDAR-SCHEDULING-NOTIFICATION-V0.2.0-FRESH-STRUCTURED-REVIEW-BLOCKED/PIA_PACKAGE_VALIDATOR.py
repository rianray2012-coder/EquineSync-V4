#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> int:
    errors = []
    required = [
        "ES-PIA-TASK-CALENDAR-SCHEDULING-NOTIFICATION_V0_1_PREDECESSOR.md",
        "ES-PIA-TASK-CALENDAR-SCHEDULING-NOTIFICATION_V0_2_STRENGTHENED_DRAFT.md",
        "FOUNDER_DECISION_REGISTER.csv",
        "SOURCE_REGISTER.csv",
        "REQUIREMENT_REGISTER.csv",
        "ACCEPTANCE_CRITERIA.csv",
        "TEST_MATRIX.csv",
        "REVISED_TRACEABILITY_MATRIX.csv",
        "FIVE_QUESTION_RESPONSE_MATRIX.csv",
        "STRUCTURED_REVIEW_REPORT.md",
        "DETERMINISTIC_VALIDATION_REPORT.json",
        "PACKAGE_MANIFEST.json",
        "CHECKSUM_MANIFEST.sha256",
        "COMPLETION_RECEIPT.md",
    ]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append(f"missing {name}")
    text = (ROOT / "ES-PIA-TASK-CALENDAR-SCHEDULING-NOTIFICATION_V0_2_STRENGTHENED_DRAFT.md").read_text(encoding="utf-8")
    nums = [int(n) for n in re.findall(r"^## ([0-9]+)\. ", text, re.M)]
    if nums != list(range(1, 44)):
        errors.append("candidate sections are not contiguous 1-43")
    decisions = read_csv(ROOT / "FOUNDER_DECISION_REGISTER.csv")
    if [row["decision_id"] for row in decisions] != [f"TCSN-FD-{i:03d}" for i in range(1, 21)]:
        errors.append("Founder decisions are not TCSN-FD-001 through TCSN-FD-020")
    for name, expected in [("REQUIREMENT_REGISTER.csv", 120), ("ACCEPTANCE_CRITERIA.csv", 55), ("TEST_MATRIX.csv", 65)]:
        rows = read_csv(ROOT / name)
        if len(rows) != expected:
            errors.append(f"{name}: expected {expected}, found {len(rows)}")
    data = json.loads((ROOT / "DETERMINISTIC_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    if data.get("runtime_gate") != "FAIL_FOR_FORMAL_REVIEW":
        errors.append("runtime gate must remain FAIL_FOR_FORMAL_REVIEW")
    if data.get("independent_review_claimed"):
        errors.append("independent review must not be claimed")
    entries = []
    for line in (ROOT / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        entries.append((digest, rel))
    for expected_digest, rel in entries:
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if actual != expected_digest:
            errors.append(f"checksum mismatch {rel}")
    print("ITEM 06 TCSN PACKAGE VALIDATION")
    print(f"files_checked={len(entries)}")
    for error in errors:
        print(f"ERROR: {error}")
    print("RESULT:", "PASS" if not errors else "FAIL")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
