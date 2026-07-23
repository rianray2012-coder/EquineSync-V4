#!/usr/bin/env python3
"""Deterministic structural checks for the Remaining PIA program inventory package."""
from __future__ import annotations

import csv
import hashlib
import json
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
    "REMAINING_PIAS_FOUNDER_APPROVAL_RECORD_2026-07-22.md",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_V0_1_INITIAL_DRAFT.md",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_FIVE_QUESTION_RESPONSE_MATRIX.csv",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_TRACEABILITY_MATRIX.csv",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_INITIAL_OPEN_ISSUES_REGISTER.csv",
    "BATCH_01_FOUNDATIONAL/ITEM_03_INITIAL_DRAFT_V0_1/REVIEW_GATE.md",
}

ITEM03_V02_REL = "BATCH_01_FOUNDATIONAL/ITEM_03_STRENGTHENED_V0_2"
ITEM03_V02_REQUIRED = {
    "ACCEPTANCE_CRITERIA.csv",
    "ADVERSARIAL_SCENARIOS.md",
    "API_EVENT_JOB_CONTRACTS.md",
    "ARTIFACT_MANIFEST.json",
    "AUDIT_AND_EVIDENCE_REQUIREMENTS.csv",
    "AUTHORIZATION_INPUT_REGISTER.csv",
    "CHECKSUM_LEDGER.sha256",
    "ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE.md",
    "FINDING_DISPOSITION_MATRIX.csv",
    "FIVE_QUESTION_RESPONSE_MATRIX.csv",
    "FOUNDER_DECISION_TRACEABILITY_MATRIX.csv",
    "GOLDEN_PATHS.md",
    "OFFLINE_AND_SYNCHRONIZATION_REQUIREMENTS.md",
    "PERMISSION_EVALUATION_CONTRACT.md",
    "PERMISSION_MATRIX.csv",
    "PRIVACY_SAFEGUARDING_RECORDS_CLAIMS_CROSSWALK.csv",
    "PROVIDER_RELATIONSHIP_AND_AUTHORITY_CONTRACT.md",
    "RELATIONSHIP_TYPE_REGISTER.csv",
    "REPRESENTATION_AND_DELEGATION_REGISTER.csv",
    "REQUIREMENT_REGISTER.csv",
    "RESTRICTION_AND_REVOCATION_REGISTER.csv",
    "REVISED_TRACEABILITY_MATRIX.csv",
    "REVISION_CHANGELOG.csv",
    "SOURCE_REGISTER.csv",
    "STATE_TRANSITION_MATRIX.csv",
    "TEST_MATRIX.csv",
    "UNRESOLVED_ITEMS_REGISTER.csv",
    "VALIDATION_REPORT.md",
}

ITEM04_REL = "BATCH_02_HORSE_DOMAIN/ITEM_04_FOUNDER_APPROVED_V0_3"
ITEM04_REQUIRED = {
    "ACCEPTANCE_CRITERIA.csv",
    "ADVERSARIAL_SCENARIOS.md",
    "ARTIFACT_MANIFEST.json",
    "AUDIT_AND_EVIDENCE_REQUIREMENTS.csv",
    "CHECKSUM_LEDGER.sha256",
    "DUPLICATE_MERGE_UNMERGE_CONTRACT.md",
    "ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md",
    "FIVE_QUESTION_RESPONSE_MATRIX.csv",
    "FOUNDER_APPROVAL_RECORD_ITEM_04_V0_3.md",
    "FOUNDER_DECISION_REGISTER.csv",
    "FOUNDER_DECISION_TRACEABILITY_MATRIX.csv",
    "GOLDEN_PATHS.md",
    "OFFLINE_AND_SYNCHRONIZATION_REQUIREMENTS.md",
    "PASSPORT_AND_EXPORT_CONTRACT.md",
    "PRIVACY_RECORDS_CLAIMS_CROSSWALK.csv",
    "REQUIREMENT_REGISTER.csv",
    "REVISED_TRACEABILITY_MATRIX.csv",
    "REVIEW_GATE.md",
    "SOURCE_REGISTER.csv",
    "STATE_TRANSITION_MATRIX.csv",
    "TEST_MATRIX.csv",
    "TRANSFER_EFFECTIVE_TIME_AND_CONTINUITY_CONTRACT.md",
    "UNRESOLVED_ITEMS_REGISTER.csv",
    "VALIDATION_REPORT.md",
    "VERSION_LINEAGE.csv",
}

QUESTIONS = [
    "Can engineering build the capability without making unauthorized product decisions?",
    "Can quality assurance determine objectively whether the capability works?",
    "Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?",
    "Can EquineSync safely operate, support, monitor, recover, and maintain the capability?",
    "Can the Founder determine whether the capability is ready for first-user enrollment?",
]

EXPECTED_TOTAL_FILES = 148
EXPECTED_CHECKSUMMED_FILES = 147
MANIFEST_NAME = "REMAINING_PIA_FILE_MANIFEST.txt"
CHECKSUM_LEDGER_NAME = "REMAINING_PIA_CHECKSUMS.sha256"
ITEM04_DISPOSITION = (
    "ITEM_04_V0_3_FOUNDER_APPROVED_DOCUMENTARY_DESIGN_ONLY_"
    "PENDING_COMPLIANT_FRESH_REVIEW"
)
ITEM04_V03_SHA256 = "daae9b0ebe1551217a96c0cb640939752807d12c1e2241f0a936bb9ce14a21e5"


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


def ids(value: str, prefix: str) -> set[str]:
    return set(re.findall(rf"{re.escape(prefix)}[0-9]+", value or ""))


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
    expected_decisions = {
        "ES-PIA-GFD-001",
        "ES-PIA-GFD-002",
        "ES-PIA-GFD-003",
        "ES-PIA-GFD-004",
        "ES-PIA-GFD-007",
    }
    if {row.get("decision_id") for row in decisions} != expected_decisions:
        errors.append("Founder decision register must contain the five approved decision IDs exactly")
    for row in decisions:
        if row.get("status") != "FOUNDER_APPROVED_DOCUMENTARY_DESIGN_ONLY":
            errors.append(
                f"{row.get('decision_id')}: status is not "
                "FOUNDER_APPROVED_DOCUMENTARY_DESIGN_ONLY"
            )
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

    item03_v02 = root / ITEM03_V02_REL
    item03_v02_paths = sorted(path for path in item03_v02.glob("*") if path.is_file())
    item03_v02_files = [path.name for path in item03_v02_paths]
    if set(item03_v02_files) != ITEM03_V02_REQUIRED or len(item03_v02_files) != 28:
        errors.append("Item 03 V0.2 must contain exactly the 28 required files")

    item03_v02_main_path = item03_v02 / (
        "ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION_V0_2_"
        "STRENGTHENED_DOCUMENTARY_CANDIDATE.md"
    )
    item03_v02_text = (
        item03_v02_main_path.read_text(encoding="utf-8")
        if item03_v02_main_path.is_file()
        else ""
    )
    item03_v02_sections = [
        int(match.group(1))
        for match in re.finditer(r"^## ([0-9]+)\. ", item03_v02_text, re.MULTILINE)
    ]
    if item03_v02_sections != list(range(1, 44)):
        errors.append("Item 03 V0.2 must contain exactly ordered sections 1 through 43")
    for question in QUESTIONS:
        if question not in item03_v02_text:
            errors.append(f"Item 03 V0.2 missing exact readiness question: {question}")
    required_v02_statements = [
        "**Implementation Authority:** `FALSE`",
        "**Independent review completed:** `FALSE`",
        "ITEM_03_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW",
        "Provider connection, profile status, API access, appointment participation, payment, or portal visibility",
        "No runtime is provisioned or launched",
    ]
    for statement in required_v02_statements:
        if statement not in item03_v02_text:
            errors.append(f"Item 03 V0.2 missing required boundary statement: {statement}")
    if re.search(r"\bMAIP\b", item03_v02_text):
        errors.append("Legacy acronym MAIP appears in active Item 03 V0.2 draft")

    v02_questions = csv_rows.get(f"{ITEM03_V02_REL}/FIVE_QUESTION_RESPONSE_MATRIX.csv", [])
    if [row.get("question_text") for row in v02_questions] != QUESTIONS:
        errors.append("Item 03 V0.2 five-question matrix must preserve exact wording and order")
    expected_v02_answers = ["NO", "PARTIALLY_SATISFIED", "PARTIALLY_SATISFIED", "NO", "NO"]
    if [row.get("answer") for row in v02_questions] != expected_v02_answers:
        errors.append("Item 03 V0.2 five-question answers differ from the controlled result")

    key_map = {
        "SOURCE_REGISTER.csv": "source_id",
        "REQUIREMENT_REGISTER.csv": "requirement_id",
        "RELATIONSHIP_TYPE_REGISTER.csv": "relationship_type_id",
        "REPRESENTATION_AND_DELEGATION_REGISTER.csv": "rule_id",
        "AUTHORIZATION_INPUT_REGISTER.csv": "input_id",
        "RESTRICTION_AND_REVOCATION_REGISTER.csv": "control_id",
        "STATE_TRANSITION_MATRIX.csv": "transition_id",
        "PERMISSION_MATRIX.csv": "permission_rule_id",
        "AUDIT_AND_EVIDENCE_REQUIREMENTS.csv": "evidence_id",
        "PRIVACY_SAFEGUARDING_RECORDS_CLAIMS_CROSSWALK.csv": "crosswalk_id",
        "ACCEPTANCE_CRITERIA.csv": "acceptance_id",
        "TEST_MATRIX.csv": "test_id",
        "UNRESOLVED_ITEMS_REGISTER.csv": "unresolved_id",
        "FINDING_DISPOSITION_MATRIX.csv": "finding_id",
        "REVISION_CHANGELOG.csv": "change_id",
        "FOUNDER_DECISION_TRACEABILITY_MATRIX.csv": "decision_id",
    }
    for filename, key in key_map.items():
        unique(
            csv_rows.get(f"{ITEM03_V02_REL}/{filename}", []),
            key,
            f"Item 03 V0.2 {filename}",
            errors,
        )

    v02_sources = {
        row.get("source_id", "")
        for row in csv_rows.get(f"{ITEM03_V02_REL}/SOURCE_REGISTER.csv", [])
    }
    v02_requirements = {
        row.get("requirement_id", "")
        for row in csv_rows.get(f"{ITEM03_V02_REL}/REQUIREMENT_REGISTER.csv", [])
    }
    v02_acceptance = {
        row.get("acceptance_id", "")
        for row in csv_rows.get(f"{ITEM03_V02_REL}/ACCEPTANCE_CRITERIA.csv", [])
    }
    v02_tests = {
        row.get("test_id", "")
        for row in csv_rows.get(f"{ITEM03_V02_REL}/TEST_MATRIX.csv", [])
    }
    v02_unresolved = {
        row.get("unresolved_id", "")
        for row in csv_rows.get(f"{ITEM03_V02_REL}/UNRESOLVED_ITEMS_REGISTER.csv", [])
    }
    for relative, rows in csv_rows.items():
        if not relative.startswith(f"{ITEM03_V02_REL}/"):
            continue
        for line_number, row in enumerate(rows, 2):
            joined = ";".join(row.values())
            for found in ids(joined, "RAP-SRC-"):
                if found not in v02_sources:
                    errors.append(f"{relative}:{line_number}: unknown source {found}")
            for found in ids(joined, "RAP-REQ-"):
                if found not in v02_requirements:
                    errors.append(f"{relative}:{line_number}: unknown requirement {found}")
            for found in ids(joined, "RAP-AC-"):
                if found not in v02_acceptance:
                    errors.append(f"{relative}:{line_number}: unknown acceptance criterion {found}")
            for found in ids(joined, "RAP-TST-"):
                if found not in v02_tests:
                    errors.append(f"{relative}:{line_number}: unknown test {found}")
            for found in ids(joined, "RAP-UNR-"):
                if found not in v02_unresolved:
                    errors.append(f"{relative}:{line_number}: unknown unresolved item {found}")
            for found in re.findall(r"ES-PIA-GFD-[0-9]+", joined):
                if found not in expected_decisions:
                    errors.append(f"{relative}:{line_number}: unknown Founder decision {found}")

    v02_trace = csv_rows.get(f"{ITEM03_V02_REL}/REVISED_TRACEABILITY_MATRIX.csv", [])
    if [row.get("section") for row in v02_trace] != [str(n) for n in range(1, 44)]:
        errors.append("Item 03 V0.2 traceability matrix must contain sections 1 through 43")

    manifest = item03_v02 / "ARTIFACT_MANIFEST.json"
    if manifest.is_file():
        try:
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
            manifest_files = [entry["filename"] for entry in manifest_data.get("files", [])]
            if manifest_data.get("total_package_files") != 28:
                errors.append("Item 03 V0.2 manifest total_package_files must be 28")
            if manifest_data.get("checksum_covered_files") != 27:
                errors.append("Item 03 V0.2 manifest checksum_covered_files must be 27")
            if sorted(manifest_files) != sorted(item03_v02_files):
                errors.append("Item 03 V0.2 manifest does not match package filenames")
            if len(manifest_files) != len(set(manifest_files)):
                errors.append("Item 03 V0.2 manifest contains duplicate filenames")
        except Exception as exc:
            errors.append(f"Item 03 V0.2 manifest invalid: {exc}")

    v02_ledger = item03_v02 / "CHECKSUM_LEDGER.sha256"
    v02_ledger_files: list[str] = []
    if v02_ledger.is_file():
        for line_number, line in enumerate(v02_ledger.read_text(encoding="utf-8").splitlines(), 1):
            try:
                digest, filename = line.split("  ", 1)
            except ValueError:
                errors.append(f"Item 03 V0.2 checksum line {line_number}: invalid format")
                continue
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"Item 03 V0.2 checksum line {line_number}: invalid SHA-256")
                continue
            v02_ledger_files.append(filename)
            target = item03_v02 / filename
            if not target.is_file():
                errors.append(f"Item 03 V0.2 checksum target missing: {filename}")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append(f"Item 03 V0.2 checksum mismatch: {filename}")
        expected_v02_covered = sorted(name for name in item03_v02_files if name != v02_ledger.name)
        if len(v02_ledger_files) != 27:
            errors.append("Item 03 V0.2 checksum ledger must contain exactly 27 entries")
        if len(v02_ledger_files) != len(set(v02_ledger_files)):
            errors.append("Item 03 V0.2 checksum ledger contains duplicate filenames")
        if v02_ledger.name in v02_ledger_files:
            errors.append("Item 03 V0.2 checksum ledger must intentionally self-exclude")
        if sorted(v02_ledger_files) != expected_v02_covered:
            errors.append("Item 03 V0.2 checksum ledger coverage mismatch")

    item04 = root / ITEM04_REL
    item04_paths = sorted(path for path in item04.glob("*") if path.is_file())
    item04_files = [path.name for path in item04_paths]
    if set(item04_files) != ITEM04_REQUIRED or len(item04_files) != 25:
        errors.append("Item 04 V0.3 must contain exactly the 25 required files")

    item04_main_path = (
        item04
        / "ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md"
    )
    item04_text = (
        item04_main_path.read_text(encoding="utf-8")
        if item04_main_path.is_file()
        else ""
    )
    if item04_main_path.is_file():
        actual_v03_hash = hashlib.sha256(item04_main_path.read_bytes()).hexdigest()
        if actual_v03_hash != ITEM04_V03_SHA256:
            errors.append("Item 04 V0.3 approved artifact SHA-256 mismatch")
    item04_sections = [
        int(match.group(1))
        for match in re.finditer(r"^## ([0-9]+)\. ", item04_text, re.MULTILINE)
    ]
    if item04_sections != list(range(1, 44)):
        errors.append("Item 04 V0.3 must contain exactly ordered sections 1 through 43")
    for question in QUESTIONS:
        if question not in item04_text:
            errors.append(f"Item 04 V0.3 missing exact readiness question: {question}")
    required_item04_statements = [
        "**Formal independent review:** `NOT_STARTED`",
        "**Founder approval of V0.3:** `NOT_REQUESTED`",
        "**Implementation:** `FALSE`",
        "**Schema:** `FALSE`",
        "**Migration:** `FALSE`",
        "**Deployment:** `FALSE`",
        "**Production use:** `FALSE`",
        "**Enrollment:** `FALSE`",
        "NO_IMPLEMENTATION_NO_SCHEMA_NO_MIGRATION_NO_DEPLOYMENT_NO_PRODUCTION_NO_ENROLLMENT",
    ]
    for statement in required_item04_statements:
        if statement not in item04_text:
            errors.append(f"Item 04 V0.3 missing preserved boundary statement: {statement}")

    item04_questions = csv_rows.get(f"{ITEM04_REL}/FIVE_QUESTION_RESPONSE_MATRIX.csv", [])
    if [row.get("question") for row in item04_questions] != QUESTIONS:
        errors.append("Item 04 five-question matrix must preserve exact wording and order")
    expected_item04_answers = ["NO", "PARTIALLY_SATISFIED", "PARTIALLY_SATISFIED", "NO", "NO"]
    if [row.get("answer") for row in item04_questions] != expected_item04_answers:
        errors.append("Item 04 five-question answers differ from the controlled result")

    item04_key_map = {
        "SOURCE_REGISTER.csv": "source_id",
        "REQUIREMENT_REGISTER.csv": "requirement_id",
        "STATE_TRANSITION_MATRIX.csv": "transition_id",
        "AUDIT_AND_EVIDENCE_REQUIREMENTS.csv": "evidence_id",
        "PRIVACY_RECORDS_CLAIMS_CROSSWALK.csv": "crosswalk_id",
        "ACCEPTANCE_CRITERIA.csv": "acceptance_id",
        "TEST_MATRIX.csv": "test_id",
        "UNRESOLVED_ITEMS_REGISTER.csv": "unresolved_id",
        "FOUNDER_DECISION_REGISTER.csv": "decision_id",
        "FOUNDER_DECISION_TRACEABILITY_MATRIX.csv": "decision_id",
    }
    for filename, key in item04_key_map.items():
        unique(
            csv_rows.get(f"{ITEM04_REL}/{filename}", []),
            key,
            f"Item 04 V0.3 {filename}",
            errors,
        )

    item04_sources = {
        row.get("source_id", "")
        for row in csv_rows.get(f"{ITEM04_REL}/SOURCE_REGISTER.csv", [])
    }
    item04_requirements = {
        row.get("requirement_id", "")
        for row in csv_rows.get(f"{ITEM04_REL}/REQUIREMENT_REGISTER.csv", [])
    }
    item04_acceptance = {
        row.get("acceptance_id", "")
        for row in csv_rows.get(f"{ITEM04_REL}/ACCEPTANCE_CRITERIA.csv", [])
    }
    item04_tests = {
        row.get("test_id", "")
        for row in csv_rows.get(f"{ITEM04_REL}/TEST_MATRIX.csv", [])
    }
    item04_unresolved = {
        row.get("unresolved_id", "")
        for row in csv_rows.get(f"{ITEM04_REL}/UNRESOLVED_ITEMS_REGISTER.csv", [])
    }
    item04_decisions = {
        row.get("decision_id", "")
        for row in csv_rows.get(f"{ITEM04_REL}/FOUNDER_DECISION_REGISTER.csv", [])
    }
    if len(item04_sources) != 12:
        errors.append("Item 04 source register must contain exactly 12 sources")
    if len(item04_requirements) != 120:
        errors.append("Item 04 requirement register must contain exactly 120 requirements")
    if len(item04_acceptance) != 50:
        errors.append("Item 04 acceptance matrix must contain exactly 50 criteria")
    if len(item04_tests) != 60:
        errors.append("Item 04 test matrix must contain exactly 60 tests")
    expected_item04_decisions = {f"HOR-FD-{number:03d}" for number in range(1, 18)}
    if item04_decisions != expected_item04_decisions:
        errors.append("Item 04 Founder decision register must contain HOR-FD-001 through HOR-FD-017 exactly")
    for row in csv_rows.get(f"{ITEM04_REL}/FOUNDER_DECISION_REGISTER.csv", []):
        if row.get("approval_status") != "FOUNDER_APPROVED_DOCUMENTARY_DESIGN_ONLY":
            errors.append(f"{row.get('decision_id')}: Item 04 decision status is not documentary-only")
    for row in csv_rows.get(f"{ITEM04_REL}/TEST_MATRIX.csv", []):
        if row.get("execution_status") != "DESIGN_TEST_DEFINED_NOT_EXECUTED":
            errors.append(f"{row.get('test_id')}: Item 04 test is not marked unexecuted")

    for relative, rows in csv_rows.items():
        if not relative.startswith(f"{ITEM04_REL}/"):
            continue
        for line_number, row in enumerate(rows, 2):
            joined = ";".join(row.values())
            for found in ids(joined, "HOR-SRC-"):
                if found not in item04_sources:
                    errors.append(f"{relative}:{line_number}: unknown Item 04 source {found}")
            for found in ids(joined, "HOR-REQ-"):
                if found not in item04_requirements:
                    errors.append(f"{relative}:{line_number}: unknown Item 04 requirement {found}")
            for found in ids(joined, "HOR-AC-"):
                if found not in item04_acceptance:
                    errors.append(f"{relative}:{line_number}: unknown Item 04 acceptance criterion {found}")
            for found in ids(joined, "HOR-TST-"):
                if found not in item04_tests:
                    errors.append(f"{relative}:{line_number}: unknown Item 04 test {found}")
            for found in ids(joined, "HOR-UNR-"):
                if found not in item04_unresolved:
                    errors.append(f"{relative}:{line_number}: unknown Item 04 unresolved item {found}")
            for found in ids(joined, "HOR-FD-"):
                if found not in item04_decisions:
                    errors.append(f"{relative}:{line_number}: unknown Item 04 Founder decision {found}")

    item04_trace = csv_rows.get(f"{ITEM04_REL}/REVISED_TRACEABILITY_MATRIX.csv", [])
    if [row.get("section") for row in item04_trace] != [str(n) for n in range(1, 44)]:
        errors.append("Item 04 traceability matrix must contain sections 1 through 43")

    item04_approval_record = item04 / "FOUNDER_APPROVAL_RECORD_ITEM_04_V0_3.md"
    item04_approval_text = (
        item04_approval_record.read_text(encoding="utf-8")
        if item04_approval_record.is_file()
        else ""
    )
    required_approval_fragments = [
        ITEM04_DISPOSITION,
        "The Founder approves the documentary design expressed in Item 04 V0.3",
        "V0.3 bytes remain unchanged",
        "formal or independent review completion",
        "implementation or engineering execution",
    ]
    for fragment in required_approval_fragments:
        if fragment not in item04_approval_text:
            errors.append(f"Item 04 approval record missing required fragment: {fragment}")

    item04_review_gate = item04 / "REVIEW_GATE.md"
    item04_review_gate_text = (
        item04_review_gate.read_text(encoding="utf-8")
        if item04_review_gate.is_file()
        else ""
    )
    for fragment in [
        ITEM04_DISPOSITION,
        "| Compliant fresh independent review | `NOT_STARTED` |",
        "| Implementation authority | `FALSE` |",
        "| First-user enrollment | `FALSE` |",
    ]:
        if fragment not in item04_review_gate_text:
            errors.append(f"Item 04 review gate missing required fragment: {fragment}")

    item04_manifest = item04 / "ARTIFACT_MANIFEST.json"
    if item04_manifest.is_file():
        try:
            item04_manifest_data = json.loads(item04_manifest.read_text(encoding="utf-8"))
            manifest_files = [entry["filename"] for entry in item04_manifest_data.get("files", [])]
            if item04_manifest_data.get("total_package_files") != 25:
                errors.append("Item 04 manifest total_package_files must be 25")
            if item04_manifest_data.get("checksum_covered_files") != 24:
                errors.append("Item 04 manifest checksum_covered_files must be 24")
            if sorted(manifest_files) != sorted(item04_files):
                errors.append("Item 04 manifest does not match package filenames")
            if item04_manifest_data.get("approved_artifact_sha256") != ITEM04_V03_SHA256:
                errors.append("Item 04 manifest approved artifact hash mismatch")
            manifest_counts = item04_manifest_data.get("counts", {})
            expected_counts = {
                "canonical_sections": 43,
                "sources": 12,
                "requirements": 120,
                "acceptance_criteria": 50,
                "design_tests": 60,
                "golden_paths": 10,
                "adversarial_scenarios": 40,
                "founder_decisions": 17,
                "state_axes": 10,
            }
            for key, expected in expected_counts.items():
                if manifest_counts.get(key) != expected:
                    errors.append(f"Item 04 manifest count {key} must be {expected}")
        except Exception as exc:
            errors.append(f"Item 04 manifest invalid: {exc}")

    item04_ledger = item04 / "CHECKSUM_LEDGER.sha256"
    item04_ledger_files: list[str] = []
    if item04_ledger.is_file():
        for line_number, line in enumerate(item04_ledger.read_text(encoding="utf-8").splitlines(), 1):
            try:
                digest, filename = line.split("  ", 1)
            except ValueError:
                errors.append(f"Item 04 checksum line {line_number}: invalid format")
                continue
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"Item 04 checksum line {line_number}: invalid SHA-256")
                continue
            item04_ledger_files.append(filename)
            target = item04 / filename
            if not target.is_file():
                errors.append(f"Item 04 checksum target missing: {filename}")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append(f"Item 04 checksum mismatch: {filename}")
        expected_item04_covered = sorted(name for name in item04_files if name != item04_ledger.name)
        if len(item04_ledger_files) != 24:
            errors.append("Item 04 checksum ledger must contain exactly 24 entries")
        if len(item04_ledger_files) != len(set(item04_ledger_files)):
            errors.append("Item 04 checksum ledger contains duplicate filenames")
        if item04_ledger.name in item04_ledger_files:
            errors.append("Item 04 checksum ledger must intentionally self-exclude")
        if sorted(item04_ledger_files) != expected_item04_covered:
            errors.append("Item 04 checksum ledger coverage mismatch")

    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in root.rglob("*.md")
    )
    if "Implementation authority:** `TRUE`" in text:
        errors.append("Implementation authority TRUE detected")
    exact_approval = (
        "Founder approves ES-PIA-GFD-001, ES-PIA-GFD-002, ES-PIA-GFD-003, "
        "ES-PIA-GFD-004, and ES-PIA-GFD-007 as recommended. This is documentary "
        "design approval only and does not authorize implementation, migration, "
        "deployment, activation, enrollment, or production use."
    )
    approval_record = root / "REMAINING_PIAS_FOUNDER_APPROVAL_RECORD_2026-07-22.md"
    approval_text = approval_record.read_text(encoding="utf-8") if approval_record.is_file() else ""
    if exact_approval not in approval_text:
        errors.append("Founder approval record does not preserve the exact approval statement")
    prohibited_claims = [
        "**Implementation Authority:** `TRUE`",
        "**Independent review completed:** `TRUE`",
        "FRESH_SEGREGATED_REVIEW_COMPLETE",
        "ITEM_03_V0_2_ADOPTED",
        "ITEM_03_V0_2_RATIFIED",
    ]
    for claim in prohibited_claims:
        if claim in item03_v02_text:
            errors.append(f"Item 03 V0.2 prohibited authority/review claim: {claim}")

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
    print(f"Item 03 V0.2 files: {len(item03_v02_files)}")
    print(f"Item 03 V0.2 checksum-covered files: {len(v02_ledger_files)}")
    print("Item 03 V0.2 checksum ledger self-excluded: CHECKSUM_LEDGER.sha256")
    print(f"Item 04 V0.3 files: {len(item04_files)}")
    print(f"Item 04 V0.3 checksum-covered files: {len(item04_ledger_files)}")
    print("Item 04 V0.3 checksum ledger self-excluded: CHECKSUM_LEDGER.sha256")
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
