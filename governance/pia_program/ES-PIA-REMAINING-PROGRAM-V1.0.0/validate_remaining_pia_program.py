#!/usr/bin/env python3
"""Deterministic structural checks for the Remaining PIA program inventory package."""
from __future__ import annotations

import csv
from pathlib import Path
import re
import sys


REQUIRED = {
    "REMAINING_PIA_PROGRAM_README.md",
    "PIA_SOURCE_AND_AUTHORITY_INVENTORY.md",
    "PIA_MASTER_TEMPLATE_IDENTIFICATION.md",
    "PIA_FIVE_QUESTION_FRAMEWORK_IDENTIFICATION.md",
    "PIA_EXISTING_AND_REMAINING_INVENTORY.csv",
    "PIA_SOURCE_CONFLICT_REGISTER.csv",
    "REMAINING_PIA_MASTER_REGISTER.csv",
    "REMAINING_PIA_SCOPE_MAP.md",
    "REMAINING_PIA_RECOMMENDED_SEQUENCE.md",
    "PIA_RECOMMENDED_SEQUENCE.md",
    "REMAINING_PIA_DEPENDENCY_GRAPH.md",
    "REMAINING_PIA_DEPENDENCY_MATRIX.csv",
    "PIA_OVERLAP_AND_DEPENDENCY_MATRIX.csv",
    "REMAINING_PIA_COMPLETION_DASHBOARD.csv",
    "REMAINING_PIA_GLOBAL_RISK_REGISTER.csv",
    "REMAINING_PIAS_GLOBAL_FOUNDER_DECISION_REGISTER.csv",
    "REMAINING_PIA_GLOBAL_FOUNDER_DECISION_REGISTER.csv",
    "REMAINING_PIAS_FOUNDER_DECISION_BOOK.md",
    "REMAINING_PIA_FOUNDER_DECISION_BOOK.md",
    "REMAINING_PIAS_RECOMMENDED_DECISION_SEQUENCE.md",
    "REMAINING_PIA_SOURCE_AND_AUTHORITY_INVENTORY.md",
    "REMAINING_PIA_TRACEABILITY_INDEX.csv",
    "PROGRAM_RUNTIME_PERMISSION_RECORDS.csv",
    "PROGRAM_REVIEW_RUNTIME_GATE.md",
    "REMAINING_PIA_VALIDATION_REPORT.md",
    "REMAINING_PIA_FINAL_STATUS_REPORT.md",
    "REMAINING_PIA_FILE_MANIFEST.txt",
    "REMAINING_PIA_CHECKSUMS.sha256",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_V0_1_INITIAL_DRAFT.md",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_FIVE_QUESTION_RESPONSE_MATRIX.csv",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_TRACEABILITY_MATRIX.csv",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_OPEN_ISSUES_REGISTER.csv",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/REVIEW_GATE.md",
}

QUESTIONS = [
    "Can engineering build the capability without making unauthorized product decisions?",
    "Can quality assurance determine objectively whether the capability works?",
    "Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?",
    "Can EquineSync safely operate, support, monitor, recover, and maintain the capability?",
    "Can the Founder determine whether the capability is ready for first-user enrollment?",
]

EXPECTED_TOTAL_FILES = 90
EXPECTED_CHECKSUMMED_FILES = 89
MANIFEST_NAME = "REMAINING_PIA_FILE_MANIFEST.txt"
CHECKSUM_LEDGER_NAME = "REMAINING_PIA_CHECKSUMS.sha256"


def read_csv(path: Path, errors: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or any(not name for name in reader.fieldnames):
                errors.append(f"{path.name}: invalid header")
                return []
            rows = list(reader)
            for index, row in enumerate(rows, 2):
                if None in row or any(value is None for value in row.values()):
                    errors.append(f"{path.name}:{index}: inconsistent column count")
            return rows
    except Exception as exc:
        errors.append(f"{path.name}: {exc}")
        return []


def unique(rows: list[dict[str, str]], key: str, label: str, errors: list[str]) -> None:
    values = [row.get(key, "") for row in rows]
    if "" in values:
        errors.append(f"{label}: blank {key}")
    if len(values) != len(set(values)):
        errors.append(f"{label}: duplicate {key}")


def main(root_arg: str) -> int:
    root = Path(root_arg).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    intentional_markdown_hard_breaks = 0

    missing = sorted(name for name in REQUIRED if not (root / name).is_file())
    errors.extend(f"Missing required file: {name}" for name in missing)

    package_paths = sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".DS_Store" not in path.parts
        and "__pycache__" not in path.parts
    )
    package_files = [path.relative_to(root).as_posix() for path in package_paths]
    if len(package_files) != EXPECTED_TOTAL_FILES:
        errors.append(
            f"Package must contain exactly {EXPECTED_TOTAL_FILES} files; "
            f"found {len(package_files)}"
        )

    manifest_path = root / MANIFEST_NAME
    if manifest_path.is_file():
        manifest_files = manifest_path.read_text(encoding="utf-8").splitlines()
        if manifest_files != package_files:
            errors.append("Program manifest does not exactly match sorted package filenames")

    ledger_path = root / CHECKSUM_LEDGER_NAME
    ledger_files: list[str] = []
    if ledger_path.is_file():
        for line_number, line in enumerate(
            ledger_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            try:
                digest, relative = line.split("  ", 1)
            except ValueError:
                errors.append(f"Checksum ledger line {line_number}: invalid format")
                continue
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"Checksum ledger line {line_number}: invalid SHA-256")
            ledger_files.append(relative)
        expected_ledger_files = sorted(
            relative for relative in package_files if relative != CHECKSUM_LEDGER_NAME
        )
        if len(ledger_files) != EXPECTED_CHECKSUMMED_FILES:
            errors.append(
                f"Checksum ledger must contain exactly {EXPECTED_CHECKSUMMED_FILES} entries; "
                f"found {len(ledger_files)}"
            )
        if len(ledger_files) != len(set(ledger_files)):
            errors.append("Checksum ledger contains duplicate filenames")
        if CHECKSUM_LEDGER_NAME in ledger_files:
            errors.append(
                f"Checksum ledger must intentionally self-exclude {CHECKSUM_LEDGER_NAME}"
            )
        if sorted(ledger_files) != expected_ledger_files:
            errors.append("Checksum ledger does not cover every non-self package file exactly once")

    for path in package_paths:
        data = path.read_bytes()
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() == ".csv" and b"\r" in data:
            errors.append(f"CSV line-ending policy violation (LF required): {relative}")
        for line_number, raw_line in enumerate(data.splitlines(), 1):
            stripped = raw_line.rstrip(b" \t")
            suffix = raw_line[len(stripped):]
            if not suffix:
                continue
            if path.suffix.lower() == ".md" and suffix == b"  " and stripped:
                intentional_markdown_hard_breaks += 1
                continue
            errors.append(
                f"Unapproved trailing whitespace: {relative}:{line_number}"
            )

    aliases = {
        "PIA_RECOMMENDED_SEQUENCE.md": "REMAINING_PIA_RECOMMENDED_SEQUENCE.md",
        "REMAINING_PIA_GLOBAL_FOUNDER_DECISION_REGISTER.csv": "REMAINING_PIAS_GLOBAL_FOUNDER_DECISION_REGISTER.csv",
        "REMAINING_PIA_FOUNDER_DECISION_BOOK.md": "REMAINING_PIAS_FOUNDER_DECISION_BOOK.md",
    }
    for alias, counterpart in aliases.items():
        alias_path = root / alias
        counterpart_path = root / counterpart
        if alias_path.is_file() and counterpart_path.is_file() and alias_path.read_bytes() != counterpart_path.read_bytes():
            errors.append(f"Compatibility artifact drift: {alias} differs from {counterpart}")

    csv_rows: dict[str, list[dict[str, str]]] = {}
    for path in sorted(root.rglob("*.csv")):
        csv_rows[path.relative_to(root).as_posix()] = read_csv(path, errors)

    master = csv_rows.get("REMAINING_PIA_MASTER_REGISTER.csv", [])
    if [row.get("position") for row in master] != [f"{n:02d}" for n in range(1, 11)]:
        errors.append("Master register must contain positions 01 through 10 exactly once and in order")
    unique(master, "pia_id", "Master register", errors)

    dashboard = csv_rows.get("REMAINING_PIA_COMPLETION_DASHBOARD.csv", [])
    if [row.get("position") for row in dashboard] != [f"{n:02d}" for n in range(1, 11)]:
        errors.append("Completion dashboard must contain positions 01 through 10 exactly once and in order")

    inventory = csv_rows.get("PIA_EXISTING_AND_REMAINING_INVENTORY.csv", [])
    if len(inventory) < 34:
        errors.append("Assessment inventory must contain at least the 34 directed domains")

    decisions = csv_rows.get("REMAINING_PIAS_GLOBAL_FOUNDER_DECISION_REGISTER.csv", [])
    unique(decisions, "decision_id", "Founder decision register", errors)
    for row in decisions:
        if row.get("status") != "RECOMMENDED_NOT_APPROVED":
            errors.append(f"{row.get('decision_id')}: recommendation status is not RECOMMENDED_NOT_APPROVED")
        if not row.get("recommended_answer"):
            errors.append(f"{row.get('decision_id')}: missing recommended answer")

    conflicts = csv_rows.get("PIA_SOURCE_CONFLICT_REGISTER.csv", [])
    unique(conflicts, "conflict_id", "Conflict register", errors)
    traces = csv_rows.get("REMAINING_PIA_TRACEABILITY_INDEX.csv", [])
    unique(traces, "trace_id", "Traceability index", errors)

    runtime = csv_rows.get("PROGRAM_RUNTIME_PERMISSION_RECORDS.csv", [])
    if any(row.get("result") == "PASS" for row in runtime):
        errors.append("Current runtime records must not claim PASS for formal review")

    item03_rel = "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1"
    item03_main = root / item03_rel / "ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_V0_1_INITIAL_DRAFT.md"
    item03_text = item03_main.read_text(encoding="utf-8") if item03_main.is_file() else ""
    item03_sections = [
        int(match.group(1))
        for match in re.finditer(r"^## ([0-9]+)\. ", item03_text, re.MULTILINE)
    ]
    if item03_sections != list(range(1, 44)):
        errors.append("Item 03 initial draft must contain exactly ordered sections 1 through 43")
    for question in QUESTIONS:
        if question not in item03_text:
            errors.append(f"Item 03 missing exact readiness question: {question}")
    if re.search(r"\bMAIP\b", item03_text):
        errors.append("Legacy acronym MAIP appears in active Item 03 initial draft")
    if "**Implementation Authority:** `FALSE`" not in item03_text:
        errors.append("Item 03 initial draft does not explicitly deny implementation authority")

    item03_trace = csv_rows.get(
        f"{item03_rel}/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_TRACEABILITY_MATRIX.csv",
        [],
    )
    if [row.get("section") for row in item03_trace] != [str(n) for n in range(1, 44)]:
        errors.append("Item 03 initial traceability matrix must contain sections 1 through 43")
    item03_questions = csv_rows.get(
        f"{item03_rel}/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_FIVE_QUESTION_RESPONSE_MATRIX.csv",
        [],
    )
    if [row.get("question_text") for row in item03_questions] != QUESTIONS:
        errors.append("Item 03 five-question matrix must preserve exact wording and order")
    allowed_answers = {
        "YES_WITH_EVIDENCE",
        "NO",
        "PARTIALLY_SATISFIED",
        "NOT_APPLICABLE_WITH_JUSTIFICATION",
    }
    for row in item03_questions:
        if row.get("answer") not in allowed_answers:
            errors.append(f"Item 03 question {row.get('question_number')}: invalid answer value")

    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in root.rglob("*.md")
    )
    if "Implementation authority:** `TRUE`" in text:
        errors.append("Implementation authority TRUE detected")
    if "RECOMMENDED_NOT_APPROVED" not in text:
        errors.append("Founder recommendation disclaimer missing")

    if not (root / "REMAINING_PIA_FILE_MANIFEST.txt").exists():
        warnings.append("Manifest not yet generated")
    if not (root / "REMAINING_PIA_CHECKSUMS.sha256").exists():
        warnings.append("Checksums not yet generated")

    print("EQUINESYNC REMAINING PIA PROGRAM VALIDATION")
    print(f"Root: {root}")
    print(f"CSV files checked: {len(csv_rows)}")
    print(f"Portfolio positions: {len(master)}")
    print(f"Assessment rows: {len(inventory)}")
    print(f"Founder decisions: {len(decisions)}")
    print(f"Total package files: {len(package_files)}")
    print(f"Checksum-covered files: {len(ledger_files)}")
    print(f"Checksum ledger self-excluded: {CHECKSUM_LEDGER_NAME}")
    print(f"Intentional Markdown hard breaks: {intentional_markdown_hard_breaks}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print("RESULT:", "PASS" if not errors else "FAIL")
    return 0 if not errors else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_remaining_pia_program.py <program-directory>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
