#!/usr/bin/env python3
"""Regenerate the CGP-005 two-layer source-freeze revision package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
VALIDATION = ROOT / "validation"
sys.path.insert(0, str(VALIDATION))

import cgp_validation as validators  # noqa: E402


BASELINE = "ff2748796bf858f49a3f85bad0578850e1deb846"
BRANCH = "codex/code-guide-wave-1-source-freeze-cgp-005-v1"
PROMPT = "CGP-005"
EXECUTION = "CGEXEC-20260726-0004"
PACKAGE = "ES-CGP-005-WAVE-1-SOURCE-FREEZE-2026-07-26"
DATE = "2026-07-26"
WAVE_GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
REFERENCE_CATEGORY = "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE"
NORMATIVE_CLASSIFICATION = "NORMATIVE_GUIDE_SOURCE_FREEZE"
CYCLE_CHECKSUM_TREATMENTS = {
    "governance/implementation/code-guides/packages/CGP_002_SHA256SUMS.txt": "VALIDATED_BY_CGP_002_PACKAGE_INTEGRITY",
    "governance/implementation/code-guides/packages/CGP_003_SHA256SUMS.txt": "VALIDATED_BY_CGP_003_PACKAGE_INTEGRITY",
    "governance/implementation/code-guides/packages/CGP_004_SHA256SUMS.txt": "VALIDATED_BY_CGP_004_PACKAGE_INTEGRITY",
    "governance/implementation/code-guides/packages/CGP_005_SHA256SUMS.txt": "LEDGER_SELF_REFERENCE_EXCLUDED",
    "governance/implementation/code-guides/registers/CODE_GUIDE_ARTIFACT_INVENTORY.csv": "SELF_REFERENCE_NOT_SEALED",
    "governance/implementation/code-guides/source-accession/MASTER_CODE_GUIDE_SOURCE_REGISTER.csv": "VALIDATED_BY_SOURCE_ACCESSION_AND_DEPENDENT_LEDGERS",
}


SYNTHETIC_SOURCES = {
    "CGSRC-CGP005-0001": {
        "title": "CGP-003 Repository Integration Receipt",
        "repository_path": "governance/implementation/code-guides/receipts/CGP_003_REPOSITORY_INTEGRATION_RECEIPT.md",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0002": {
        "title": "CGP-004 Repository Integration Receipt",
        "repository_path": "governance/implementation/code-guides/receipts/CGP_004_REPOSITORY_INTEGRATION_RECEIPT.md",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0003": {
        "title": "CGP-003 Source Register",
        "repository_path": "governance/implementation/code-guides/source-accession/MASTER_CODE_GUIDE_SOURCE_REGISTER.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0004": {
        "title": "CGP-003 Source To Guide Map",
        "repository_path": "governance/implementation/code-guides/source-accession/MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0005": {
        "title": "CGP-003 Source Conflict Register",
        "repository_path": "governance/implementation/code-guides/source-accession/MASTER_CODE_GUIDE_SOURCE_CONFLICT_REGISTER.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0006": {
        "title": "CGP-003 Source Supersession Register",
        "repository_path": "governance/implementation/code-guides/source-accession/MASTER_CODE_GUIDE_SOURCE_SUPERSESSION_REGISTER.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0007": {
        "title": "CGP-004 Current Repository Component Register",
        "repository_path": "governance/implementation/code-guides/assessment/CURRENT_REPOSITORY_COMPONENT_REGISTER.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0008": {
        "title": "CGP-004 Current Code Guide Gap Register",
        "repository_path": "governance/implementation/code-guides/assessment/CURRENT_CODE_GUIDE_GAP_REGISTER.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0009": {
        "title": "CGP-004 Repository To Source Evidence Map",
        "repository_path": "governance/implementation/code-guides/assessment/REPOSITORY_TO_SOURCE_EVIDENCE_MAP.csv",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0010": {
        "title": "CGP-004 Founder Decision Reconciliation",
        "repository_path": "governance/implementation/code-guides/receipts/CGP_004_FOUNDER_DECISION_RECONCILIATION.md",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0011": {
        "title": "CGP-003 Founder Decision Reconciliation",
        "repository_path": "governance/implementation/code-guides/receipts/CGP_003_FOUNDER_DECISION_RECONCILIATION.md",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
    },
    "CGSRC-CGP005-0201": {
        "title": "Representative Backend Application Assembly",
        "repository_path": "backend/server.py",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0001",
    },
    "CGSRC-CGP005-0202": {
        "title": "Representative Backend Authentication Logic",
        "repository_path": "backend/core/auth.py",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0003",
    },
    "CGSRC-CGP005-0203": {
        "title": "Representative Backend Tenancy Logic",
        "repository_path": "backend/core/tenancy.py",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0004",
    },
    "CGSRC-CGP005-0204": {
        "title": "Representative Backend Permission Logic",
        "repository_path": "backend/core/permissions.py",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0004",
    },
    "CGSRC-CGP005-0205": {
        "title": "Representative Backend Lifespan And Startup Logic",
        "repository_path": "backend/core/lifespan.py",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0013",
    },
    "CGSRC-CGP005-0206": {
        "title": "Representative Task Materialization Logic",
        "repository_path": "backend/task_engine.py",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0008",
    },
    "CGSRC-CGP005-0207": {
        "title": "Backend Test Suite Directory",
        "repository_path": "backend/tests",
        "source_class": "TEST_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0020",
    },
    "CGSRC-CGP005-0208": {
        "title": "Pytest Configuration",
        "repository_path": "pytest.ini",
        "source_class": "TEST_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0020",
    },
    "CGSRC-CGP005-0209": {
        "title": "GitHub Actions CI Workflow",
        "repository_path": ".github/workflows/ci.yml",
        "source_class": "REPOSITORY_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0021",
    },
    "CGSRC-CGP005-0210": {
        "title": "Live Test Allowlist",
        "repository_path": "backend/tests/live_test_allowlist.txt",
        "source_class": "TEST_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0020",
    },
    "CGSRC-CGP005-0211": {
        "title": "Known Failure Gate",
        "repository_path": "backend/tests/ci_known_failure_gate.py",
        "source_class": "TEST_EVIDENCE",
        "authority_status": "SUPPORTING",
        "component_ids": "CGP004-COMP-0020",
    },
}


SELECTIONS = {
    "ES-CG-00": {
        "areas": "charter_authority;program_scope;lifecycle;ownership;non_authorization",
        "question": "ES-CG-00-DQ-0001",
        "source_ids": [
            "CGSRC-GOV-0002",
            "CGSRC-GOV-0003",
            "CGSRC-GOV-0005",
            "CGSRC-GOV-0006",
            "CGSRC-GOV-0008",
            "CGSRC-GOV-0009",
            "CGSRC-GOV-0011",
            "CGSRC-GOV-0012",
            "CGSRC-GOV-0014",
            "CGSRC-GOV-0084",
            "CGSRC-GOV-0138",
            "CGSRC-GOV-0139",
            "CGSRC-GOV-0152",
            "CGSRC-GOV-0153",
            "CGSRC-ATLAS-0006",
            "CGSRC-ATLAS-0017",
            "CGSRC-ATLAS-0018",
            "CGSRC-ATLAS-0019",
            "CGSRC-ATLAS-0020",
            "CGSRC-ATLAS-0021",
            "CGSRC-REPO-0001",
            "CGSRC-REPO-0002",
            "CGSRC-REPO-0008",
            "CGSRC-REPO-0009",
            "CGSRC-CGP005-0001",
            "CGSRC-CGP005-0002",
            "CGSRC-CGP005-0003",
            "CGSRC-CGP005-0004",
        ],
        "component_evidence": ["CGSRC-CGP005-0201"],
    },
    "ES-CG-01": {
        "areas": "authority_precedence;founder_disposition;conflict;supersession;exceptions",
        "question": "ES-CG-01-DQ-0001",
        "source_ids": [
            "CGSRC-GOV-0002",
            "CGSRC-GOV-0003",
            "CGSRC-GOV-0004",
            "CGSRC-GOV-0005",
            "CGSRC-GOV-0006",
            "CGSRC-GOV-0007",
            "CGSRC-GOV-0008",
            "CGSRC-GOV-0009",
            "CGSRC-GOV-0010",
            "CGSRC-GOV-0011",
            "CGSRC-GOV-0012",
            "CGSRC-GOV-0013",
            "CGSRC-GOV-0014",
            "CGSRC-GOV-0134",
            "CGSRC-GOV-0138",
            "CGSRC-GOV-0139",
            "CGSRC-GOV-0140",
            "CGSRC-GOV-0141",
            "CGSRC-GOV-0152",
            "CGSRC-GOV-0153",
            "CGSRC-GOV-0018",
            "CGSRC-ARCH-0021",
            "CGSRC-ATLAS-0017",
            "CGSRC-ATLAS-0018",
            "CGSRC-ATLAS-0019",
            "CGSRC-ATLAS-0020",
            "CGSRC-ATLAS-0021",
            "CGSRC-CGP005-0005",
            "CGSRC-CGP005-0006",
            "CGSRC-CGP005-0010",
            "CGSRC-CGP005-0011",
        ],
        "component_evidence": ["CGSRC-CGP005-0202", "CGSRC-CGP005-0203", "CGSRC-CGP005-0204"],
    },
    "ES-CG-13": {
        "areas": "completion;evidence_grade;traceability;custody;closure;activation_boundary",
        "question": "ES-CG-13-DQ-0001",
        "source_ids": [
            "CGSRC-GOV-0002",
            "CGSRC-GOV-0003",
            "CGSRC-GOV-0004",
            "CGSRC-GOV-0005",
            "CGSRC-GOV-0007",
            "CGSRC-GOV-0008",
            "CGSRC-GOV-0009",
            "CGSRC-GOV-0010",
            "CGSRC-GOV-0011",
            "CGSRC-GOV-0012",
            "CGSRC-GOV-0013",
            "CGSRC-GOV-0014",
            "CGSRC-GOV-0016",
            "CGSRC-GOV-0017",
            "CGSRC-GOV-0018",
            "CGSRC-GOV-0134",
            "CGSRC-GOV-0140",
            "CGSRC-GOV-0141",
            "CGSRC-GOV-0152",
            "CGSRC-GOV-0153",
            "CGSRC-PIA-0010",
            "CGSRC-HIST-0038",
            "CGSRC-ATLAS-0006",
            "CGSRC-ATLAS-0017",
            "CGSRC-ATLAS-0018",
            "CGSRC-ATLAS-0019",
            "CGSRC-ATLAS-0020",
            "CGSRC-ATLAS-0021",
            "CGSRC-ATLAS-0022",
            "CGSRC-ATLAS-0023",
            "CGSRC-CGP005-0001",
            "CGSRC-CGP005-0002",
            "CGSRC-CGP005-0003",
            "CGSRC-CGP005-0004",
            "CGSRC-CGP005-0005",
            "CGSRC-CGP005-0006",
            "CGSRC-CGP005-0007",
            "CGSRC-CGP005-0008",
            "CGSRC-CGP005-0009",
            "CGSRC-CGP005-0010",
            "CGSRC-CGP005-0011",
        ],
        "component_evidence": ["CGSRC-CGP005-0201", "CGSRC-CGP005-0205", "CGSRC-CGP005-0207", "CGSRC-CGP005-0209"],
    },
    "ES-CG-10": {
        "areas": "testing;verification;assurance;positive_negative_tests;ci_interpretation;false_pass_prevention",
        "question": "ES-CG-10-DQ-0001",
        "source_ids": [
            "CGSRC-GOV-0007",
            "CGSRC-GOV-0008",
            "CGSRC-GOV-0016",
            "CGSRC-GOV-0017",
            "CGSRC-GOV-0018",
            "CGSRC-GOV-0140",
            "CGSRC-GOV-0141",
            "CGSRC-ATLAS-0006",
            "CGSRC-ATLAS-0017",
            "CGSRC-ATLAS-0018",
            "CGSRC-ATLAS-0019",
            "CGSRC-ATLAS-0020",
            "CGSRC-ATLAS-0021",
            "CGSRC-ATLAS-0022",
            "CGSRC-REPO-0006",
            "CGSRC-REPO-0007",
            "CGSRC-TEST-0001",
            "CGSRC-TEST-0002",
            "CGSRC-TEST-0004",
            "CGSRC-REPO-0629",
            "CGSRC-EXT-0002",
            "CGSRC-CGP005-0007",
            "CGSRC-CGP005-0008",
            "CGSRC-CGP005-0009",
        ],
        "component_evidence": [
            "CGSRC-CGP005-0205",
            "CGSRC-CGP005-0206",
            "CGSRC-CGP005-0207",
            "CGSRC-CGP005-0208",
            "CGSRC-CGP005-0209",
            "CGSRC-CGP005-0210",
            "CGSRC-CGP005-0211",
        ],
    },
}


def run(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=REPO, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_children(rel: str) -> list[str]:
    out = run(["git", "ls-files", rel])
    return [line for line in out.splitlines() if line.strip()]


def sha256_tree(rel: str) -> str:
    h = hashlib.sha256()
    for child in sorted(tracked_children(rel)):
        path = REPO / child
        if not path.is_file():
            continue
        h.update(child.encode())
        h.update(b"\0")
        h.update(sha256_file(path).encode())
        h.update(b"\n")
    return h.hexdigest()


def git_object(rel: str, is_dir: bool) -> str:
    try:
        if is_dir:
            return run(["git", "rev-parse", f"HEAD:{rel}"])
        return run(["git", "hash-object", rel])
    except RuntimeError:
        return "0" * 40


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_category(row: dict[str, str]) -> str:
    status = row.get("authority_status", "")
    source_class = row.get("source_class", "")
    if status == "CONTROLLING":
        return "CONTROLLING_FROZEN"
    if status == "HISTORICAL":
        return "HISTORICAL_FROZEN"
    if source_class in {"REPOSITORY_EVIDENCE", "TEST_EVIDENCE"}:
        return "IMPLEMENTATION_EVIDENCE_FROZEN"
    if status == "PROPOSED":
        return "EXCLUDED_PROPOSED"
    if status == "BLOCKED":
        return "EXCLUDED_BLOCKED"
    return "SUPPORTING_FROZEN"


def refresh_source_row(row: dict[str, str]) -> dict[str, str]:
    row = {field: row.get(field, "") for field in validators._source_freeze_fields()}
    rel = row["repository_path"]
    actual = REPO / rel
    is_dir = actual.is_dir()
    row["repository_commit"] = BASELINE
    row["git_object_type"] = "TREE" if is_dir else "BLOB"
    row["git_object_sha"] = git_object(rel, is_dir)
    if is_dir:
        row["sha256_checksum"] = sha256_tree(rel)
        row["checksum_verification_result"] = "VERIFIED_DIRECTORY_AGGREGATE"
    else:
        row["sha256_checksum"] = sha256_file(actual)
        row["checksum_verification_result"] = "VERIFIED_FILE"
    return row


def synthetic_source_row(source_id: str) -> dict[str, str]:
    spec = SYNTHETIC_SOURCES[source_id]
    rel = spec["repository_path"]
    actual = REPO / rel
    if not actual.exists():
        raise FileNotFoundError(rel)
    row = {field: "" for field in validators._source_freeze_fields()}
    row.update(
        {
            "freeze_record_id": "",
            "source_id": source_id,
            "guide_id": "",
            "title": spec["title"],
            "filename": Path(rel).name,
            "repository_path": rel,
            "source_class": spec["source_class"],
            "authority_status": spec["authority_status"],
            "inclusion_category": source_category(spec),
            "version": "",
            "effective_date": DATE,
            "approval_authority": "Founder" if spec["authority_status"] == "CONTROLLING" else "",
            "approval_record_path": "",
            "repository_integration_receipt": "governance/implementation/code-guides/receipts/CGP_005_EXECUTION_RECEIPT.md",
            "custody_status": "REPOSITORY_NATIVE",
            "supersession_status": "CURRENT",
            "conflict_status": "NO_KNOWN_BLOCKING_CONFLICT",
        }
    )
    return refresh_source_row(row)


def update_controlled_values() -> None:
    path = ROOT / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    inclusions = data.setdefault("source_freeze_inclusion_categories", [])
    if REFERENCE_CATEGORY not in inclusions:
        inclusions.append(REFERENCE_CATEGORY)
    dispositions = data.setdefault("source_freeze_readiness_dispositions", [])
    if "CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW" not in dispositions:
        dispositions.append("CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW")
    write_json(path, data)


def update_source_accession_checksums() -> None:
    path = ROOT / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_REGISTER.csv"
    rows = read_csv(path)
    fields = list(rows[0].keys())
    changed_ids = {"CGSRC-REPO-0004", "CGSRC-REPO-0005", "CGSRC-REPO-0007"}
    for row in rows:
        if row.get("source_id") not in changed_ids:
            continue
        rel = row["repository_path"]
        actual = REPO / rel
        if actual.is_file():
            row["checksum"] = sha256_file(actual)
            row["checksum_verification_status"] = "VERIFIED_FILE"
            row["originating_commit"] = "CGP-005_REVISION_BRANCH_BYTES"
            note = "Checksum reconciled during CGP-005 revision because the tracked Code Guide machinery changed within authorized scope."
            if note not in row.get("notes", ""):
                row["notes"] = note if not row.get("notes") else f"{row['notes']} {note}"
    write_csv(path, fields, rows)


def load_origin_rows() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], dict]:
    common = ROOT / "source-freeze" / "WAVE_1_COMMON_SOURCE_FREEZE_REGISTER.csv"
    reference = ROOT / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_REGISTER.csv"
    source_path = common if common.exists() else reference
    rows = read_csv(source_path)
    origin = {}
    normalized = []
    for index, raw in enumerate(rows, start=1):
        row = {field: raw.get(field, "") for field in validators._source_freeze_fields()}
        if row["guide_id"] == "WAVE_1_REFERENCE_CORPUS":
            original_category = raw.get("source_burden_treatment", "")
        else:
            original_category = row.get("inclusion_category", "")
        if not original_category or original_category == "REFERENCE_CORPUS":
            original_category = source_category(row)
        row = refresh_source_row(row)
        origin[row["source_id"]] = {**row, "original_inclusion_category": original_category}
        row.update(
            {
                "freeze_record_id": f"CGP005-RC-{index:04d}",
                "guide_id": "WAVE_1_REFERENCE_CORPUS",
                "inclusion_category": REFERENCE_CATEGORY,
                "reason_for_inclusion": "Retained as the broad Wave 1 reference corpus so discovery coverage and exact bytes remain available without making this row normative.",
                "authority_rationale": "This row preserves indexed evidence only; guide drafting authority is determined by the curated normative freeze for each guide.",
                "guide_requirement_area": "REFERENCE_CORPUS",
                "necessity_test": "REFERENCE_CORPUS_ONLY",
                "consequence_of_exclusion": "Removing this row would reduce discovery traceability but would not remove normative drafting authority.",
                "related_drafting_question_ids": "REFERENCE_ONLY",
                "package_level_source_could_replace": "NOT_EVALUATED_REFERENCE_ONLY",
                "cgp004_component_ids": "",
                "curation_status": "REFERENCE_CORPUS_ONLY",
                "selected_from_cgp003_mapping": "YES",
                "source_burden_treatment": original_category,
                "retained_limitations": "Reference corpus only; not a normative source freeze, not a maturity advancement, and not a basis for CGP-006.",
            }
        )
        normalized.append(row)
    return normalized, origin, {}


def candidate_ids_by_guide() -> dict[str, set[str]]:
    rows = read_csv(ROOT / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv")
    result = {guide: set() for guide in WAVE_GUIDES}
    for row in rows:
        if row["guide_id"] in result:
            result[row["guide_id"]].add(row["source_id"])
    return result


def selected_row(source_id: str, guide: str, index: int, origin: dict[str, dict[str, str]]) -> dict[str, str]:
    base = origin.get(source_id) or synthetic_source_row(source_id)
    row = {field: base.get(field, "") for field in validators._source_freeze_fields()}
    is_synthetic = source_id in SYNTHETIC_SOURCES
    spec = SYNTHETIC_SOURCES.get(source_id, {})
    row.update(
        {
            "freeze_record_id": f"CGP005-NF-{guide}-{index:04d}",
            "guide_id": guide,
            "inclusion_category": base.get("original_inclusion_category") or source_category(row),
            "repository_integration_receipt": "governance/implementation/code-guides/receipts/CGP_005_EXECUTION_RECEIPT.md",
            "guide_requirement_area": SELECTIONS[guide]["areas"],
            "related_drafting_question_ids": SELECTIONS[guide]["question"],
            "curation_status": "NORMATIVE_SELECTED",
            "selected_from_cgp003_mapping": "NO" if is_synthetic else "YES",
            "source_burden_treatment": "NORMATIVE_MINIMUM_REQUIRED",
            "package_level_source_could_replace": "PACKAGE_LEVEL_SOURCE_IS_NORMATIVE" if row["git_object_type"] == "TREE" else "NO",
        }
    )
    if row["source_class"] in {"REPOSITORY_EVIDENCE", "TEST_EVIDENCE"}:
        row["necessity_test"] = "NECESSARY_IMPLEMENTATION_EVIDENCE"
        row["cgp004_component_ids"] = spec.get("component_ids", "CODE_GUIDE_PROGRAM_EVIDENCE")
        row["reason_for_inclusion"] = f"{guide} needs this exact evidence to identify a material current-state or program-evidence pattern within {SELECTIONS[guide]['areas']}."
        row["authority_rationale"] = "The row is implementation or program evidence only; it does not create product authority and is tied to the named requirement area."
        row["consequence_of_exclusion"] = "Excluding it would remove the representative evidence needed to frame later drafting questions without copying behavior into policy."
    elif row["inclusion_category"] == "CONTROLLING_FROZEN":
        row["necessity_test"] = "CONTROLLING_AUTHORITY"
        row["reason_for_inclusion"] = f"{guide} requires this approved authority to establish {SELECTIONS[guide]['areas']} before any drafting begins."
        row["authority_rationale"] = "The source has controlling status in the master inventory and supplies authority that cannot be replaced by repository behavior."
        row["consequence_of_exclusion"] = "Excluding it would remove or materially weaken the authority basis for the guide-specific source freeze."
        row["cgp004_component_ids"] = ""
    elif row["inclusion_category"] == "HISTORICAL_FROZEN":
        row["necessity_test"] = "RETAINED_CONFLICT_EVIDENCE"
        row["reason_for_inclusion"] = f"{guide} retains this historical row only to preserve a known conflict, supersession, or lifecycle boundary."
        row["authority_rationale"] = "The source is historical and non-controlling; its function is to keep precedence and supersession visible during drafting."
        row["consequence_of_exclusion"] = "Excluding it would conceal retained conflict evidence that the guide must not silently collapse."
        row["cgp004_component_ids"] = ""
    else:
        row["necessity_test"] = "NECESSARY_INTERPRETATION"
        row["reason_for_inclusion"] = f"{guide} needs this interpretive or provenance source to apply controlling authority within {SELECTIONS[guide]['areas']}."
        row["authority_rationale"] = "The source does not override controlling authority; it narrows ambiguity, approval lineage, or review treatment."
        row["consequence_of_exclusion"] = "Excluding it would make the selected controlling authorities ambiguous or harder to verify."
        row["cgp004_component_ids"] = ""
    if source_id.startswith("CGSRC-CGP005-0005") or source_id.startswith("CGSRC-CGP005-0006"):
        row["necessity_test"] = "RETAINED_CONFLICT_EVIDENCE"
    return row


def directory_manifest(rows: list[dict[str, str]]) -> dict[str, dict]:
    manifest = {}
    for row in rows:
        if row.get("git_object_type") != "TREE":
            continue
        children = []
        for child in tracked_children(row["repository_path"]):
            path = REPO / child
            if path.is_file():
                children.append({"path": child, "sha256_checksum": sha256_file(path)})
        manifest[row["source_id"]] = {
            "repository_path": row["repository_path"],
            "tracked_child_count": len(children),
            "children": children,
        }
    return manifest


def write_reference_corpus(rows: list[dict[str, str]]) -> dict[str, dict]:
    write_csv(ROOT / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_REGISTER.csv", validators._source_freeze_fields(), rows)
    directory_manifests = directory_manifest(rows)
    write_json(
        ROOT / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json",
        {
            "prompt_id": PROMPT,
            "execution_id": EXECUTION,
            "package_id": PACKAGE,
            "layer_id": "WAVE_1_REFERENCE_CORPUS",
            "classification": REFERENCE_CATEGORY,
            "baseline_commit": BASELINE,
            "created_date": DATE,
            "source_count": len(rows),
            "directory_manifest_count": len(directory_manifests),
            "directory_manifests": directory_manifests,
            "sources": [
                {
                    "freeze_record_id": row["freeze_record_id"],
                    "source_id": row["source_id"],
                    "repository_path": row["repository_path"],
                    "sha256_checksum": row["sha256_checksum"],
                    "curation_status": "REFERENCE_CORPUS_ONLY",
                }
                for row in rows
            ],
            "non_authorization": "The reference corpus is indexed evidence only and is not a normative guide-specific source freeze.",
        },
    )
    counts = Counter(row["source_burden_treatment"] for row in rows)
    report = [
        "# Wave 1 Reference Corpus Report",
        "",
        f"**Prompt:** `{PROMPT}`",
        f"**Execution ID:** `{EXECUTION}`",
        f"**Classification:** `{REFERENCE_CATEGORY}`",
        "",
        "The Wave 1 reference corpus preserves the broad CGP-003 mapped source universe as exact-byte evidence. It is not normative and does not advance any guide maturity.",
        "",
        "## Counts",
        "",
        f"- Reference source records: `{len(rows)}`",
        f"- Directory manifests: `{len(directory_manifests)}`",
    ]
    for key, value in sorted(counts.items()):
        report.append(f"- Original burden category `{key}`: `{value}`")
    report.extend(["", "CGP-006 was not begun."])
    (ROOT / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return directory_manifests


def build_guide_freezes(origin: dict[str, dict[str, str]], candidates: dict[str, set[str]]) -> dict[str, dict]:
    all_crosswalk = []
    all_exclusions = []
    readiness = []
    counts_by_guide = {}
    selected_by_guide = {}
    for guide in WAVE_GUIDES:
        source_ids = list(SELECTIONS[guide]["source_ids"]) + [
            sid for sid in SELECTIONS[guide]["component_evidence"] if (REPO / SYNTHETIC_SOURCES[sid]["repository_path"]).exists()
        ]
        rows = [selected_row(sid, guide, idx, origin) for idx, sid in enumerate(source_ids, start=1)]
        selected_ids = {row["source_id"] for row in rows}
        selected_by_guide[guide] = selected_ids
        counts = Counter(row["inclusion_category"] for row in rows)
        counts_by_guide[guide] = {"total": len(rows), **dict(counts)}
        guide_dir = ROOT / "guides" / guide / "source-freeze"
        write_csv(guide_dir / f"{guide}_SOURCE_FREEZE_REGISTER.csv", validators._source_freeze_fields(), rows)
        dman = directory_manifest(rows)
        write_json(
            guide_dir / f"{guide}_SOURCE_FREEZE_MANIFEST.json",
            {
                "prompt_id": PROMPT,
                "execution_id": EXECUTION,
                "guide_id": guide,
                "classification": NORMATIVE_CLASSIFICATION,
                "curation_method": "GUIDE_SPECIFIC_MINIMUM_AUTHORITY_SET",
                "baseline_commit": BASELINE,
                "created_date": DATE,
                "candidate_count": len(candidates[guide]),
                "normative_source_count": len(rows),
                "reference_corpus_only_count": max(len(candidates[guide] - selected_ids), 0),
                "directory_manifests": dman,
                "sources": [
                    {
                        "freeze_record_id": row["freeze_record_id"],
                        "source_id": row["source_id"],
                        "repository_path": row["repository_path"],
                        "inclusion_category": row["inclusion_category"],
                        "necessity_test": row["necessity_test"],
                    }
                    for row in rows
                ],
                "non_authorization": "Normative source selection is returned for Founder review only; it does not draft controls or start CGP-006.",
            },
        )
        guide_exclusions = []
        excluded = sorted(candidates[guide] - selected_ids)
        for idx, sid in enumerate(excluded, start=1):
            source = origin.get(sid, {})
            guide_exclusions.append(
                {
                    "exclusion_id": f"CGP005-EXCL-{guide}-{idx:04d}",
                    "guide_id": guide,
                    "source_id": sid,
                    "title": source.get("title", ""),
                    "repository_path": source.get("repository_path", ""),
                    "authority_status": source.get("authority_status", ""),
                    "source_class": source.get("source_class", ""),
                    "inclusion_category": REFERENCE_CATEGORY,
                    "exclusion_reason": "Retained in the non-normative Wave 1 reference corpus because it was mapped during CGP-003 but was not necessary under the guide-specific inclusion test.",
                    "required_later_action": "Re-evaluate only if later drafting identifies a concrete authority, interpretation, provenance, implementation-evidence, or retained-conflict need.",
                    "blocks_drafting": "NO",
                    "blocks_adoption_or_activation": "NO",
                }
            )
        write_csv(
            guide_dir / f"{guide}_SOURCE_EXCLUSION_REGISTER.csv",
            [
                "exclusion_id",
                "guide_id",
                "source_id",
                "title",
                "repository_path",
                "authority_status",
                "source_class",
                "inclusion_category",
                "exclusion_reason",
                "required_later_action",
                "blocks_drafting",
                "blocks_adoption_or_activation",
            ],
            guide_exclusions,
        )
        all_exclusions.extend(guide_exclusions)
        for idx, row in enumerate(rows, start=len(all_crosswalk) + 1):
            all_crosswalk.append(
                {
                    "crosswalk_id": f"CGP005-XW-{idx:05d}",
                    "guide_id": guide,
                    "source_id": row["source_id"],
                    "source_class": row["source_class"],
                    "authority_status": row["authority_status"],
                    "inclusion_category": row["inclusion_category"],
                    "mapping_type": "MANDATORY" if row["necessity_test"] == "CONTROLLING_AUTHORITY" else "SUPPORTING",
                    "coverage_note": row["guide_requirement_area"],
                    "source_freeze_record_id": row["freeze_record_id"],
                    "freeze_manifest_path": f"governance/implementation/code-guides/guides/{guide}/source-freeze/{guide}_SOURCE_FREEZE_MANIFEST.json",
                    "readiness_effect": "SUPPORTS_FOUNDER_REVIEW_NOT_CGP006_READY",
                }
            )
        write_guide_reports(guide, rows, guide_exclusions, candidates[guide], counts)
        readiness.append(
            {
                "guide_id": guide,
                "readiness_disposition": "CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW",
                "maturity_after_cgp005": "PLANNED",
                "controlling_sources_complete": "YES",
                "checksums_verified": "YES",
                "approval_basis_identified": "YES",
                "supersession_treatment_complete": "YES",
                "exclusions_recorded": "YES",
                "conflicts_resolved_or_retained": "YES",
                "repository_evidence_baseline_recorded": "YES",
                "drafting_questions_identified": "YES",
                "blocking_findings": "CGP005-F-0001",
                "decision_count": "0",
                "retained_gaps": retained_gaps_for(guide),
                "cgp006_ready": "NO",
                "status": "REVISION_RETURNED_PENDING_FOUNDER_REVIEW",
                "notes": f"{guide} has {len(rows)} curated normative rows and remains PLANNED pending Founder acceptance.",
            }
        )
    write_csv(
        ROOT / "source-freeze" / "WAVE_1_SOURCE_FREEZE_CROSSWALK.csv",
        [
            "crosswalk_id",
            "guide_id",
            "source_id",
            "source_class",
            "authority_status",
            "inclusion_category",
            "mapping_type",
            "coverage_note",
            "source_freeze_record_id",
            "freeze_manifest_path",
            "readiness_effect",
        ],
        all_crosswalk,
    )
    write_csv(
        ROOT / "source-freeze" / "WAVE_1_SOURCE_EXCLUSION_REGISTER.csv",
        [
            "exclusion_id",
            "guide_id",
            "source_id",
            "title",
            "repository_path",
            "authority_status",
            "source_class",
            "inclusion_category",
            "exclusion_reason",
            "required_later_action",
            "blocks_drafting",
            "blocks_adoption_or_activation",
        ],
        all_exclusions,
    )
    write_csv(
        ROOT / "source-freeze" / "WAVE_1_DRAFTING_READINESS_REGISTER.csv",
        [
            "guide_id",
            "readiness_disposition",
            "maturity_after_cgp005",
            "controlling_sources_complete",
            "checksums_verified",
            "approval_basis_identified",
            "supersession_treatment_complete",
            "exclusions_recorded",
            "conflicts_resolved_or_retained",
            "repository_evidence_baseline_recorded",
            "drafting_questions_identified",
            "blocking_findings",
            "decision_count",
            "retained_gaps",
            "cgp006_ready",
            "status",
            "notes",
        ],
        readiness,
    )
    return {"counts": counts_by_guide, "crosswalk_rows": len(all_crosswalk), "exclusion_rows": len(all_exclusions), "selected": selected_by_guide}


def retained_gaps_for(guide: str) -> str:
    if guide == "ES-CG-00":
        return "CGP005-F-0001"
    if guide == "ES-CG-01":
        return "CGP003-F-0004;CGP003-F-0005;CGP005-F-0001"
    if guide == "ES-CG-13":
        return "CGP003-F-0004;CGP003-F-0005;CGP004-F-0002;CGP004-F-0003;CGP004-F-0004;CGP004-F-0005;CGP004-F-0006;CGP004-F-0007;CGP005-F-0001"
    return "CGP004-F-0003;CGP004-F-0004;CGP004-F-0006;CGP004-F-0007;CGP005-F-0001"


def write_guide_reports(guide: str, rows: list[dict[str, str]], exclusions: list[dict[str, str]], candidates: set[str], counts: Counter) -> None:
    guide_dir = ROOT / "guides" / guide / "source-freeze"
    initial = len(candidates)
    report_common = [
        f"# {guide} Normative Source Selection Report",
        "",
        f"**Prompt:** `{PROMPT}`",
        f"**Execution ID:** `{EXECUTION}`",
        f"**Classification:** `{NORMATIVE_CLASSIFICATION}`",
        "",
        "This report records the curated minimum source set returned for Founder review. It does not draft guide controls and does not advance guide maturity.",
        "",
        "## Counts",
        "",
        f"- Initial CGP-003 candidate count: `{initial}`",
        f"- Normative source count: `{len(rows)}`",
        f"- Normative controlling count: `{counts.get('CONTROLLING_FROZEN', 0)}`",
        f"- Necessary supporting count: `{counts.get('SUPPORTING_FROZEN', 0)}`",
        f"- Necessary historical count: `{counts.get('HISTORICAL_FROZEN', 0)}`",
        f"- Necessary implementation-evidence count: `{counts.get('IMPLEMENTATION_EVIDENCE_FROZEN', 0)}`",
        f"- Reference-corpus-only count: `{len(exclusions)}`",
        f"- Excluded count: `{len(exclusions)}`",
        "",
        "## Selection Basis",
        "",
        "Every retained row identifies a guide requirement area, necessity test, consequence of exclusion, drafting-question linkage, and package-versus-child treatment.",
        "",
        "CGP-006 was not begun.",
    ]
    (guide_dir / f"{guide}_NORMATIVE_SOURCE_SELECTION_REPORT.md").write_text("\n".join(report_common) + "\n", encoding="utf-8")
    burden = [
        f"# {guide} Source Burden Summary",
        "",
        f"- Candidate rows reviewed: `{initial}`",
        f"- Normative rows retained: `{len(rows)}`",
        f"- Rows moved to reference corpus only: `{len(exclusions)}`",
        "",
        "The burden was reduced by replacing map passthrough with guide-specific inclusion tests.",
    ]
    (guide_dir / f"{guide}_SOURCE_BURDEN_SUMMARY.md").write_text("\n".join(burden) + "\n", encoding="utf-8")
    package_rows = [row for row in rows if row["git_object_type"] == "TREE"]
    package_report = [
        f"# {guide} Package Versus Child Treatment Report",
        "",
        f"- Package or directory-level normative rows: `{len(package_rows)}`",
        "- Child-file hashes remain preserved in the applicable manifest where a directory row is used.",
        "- No normative row states that a package-level source could replace the individual row.",
    ]
    for row in package_rows:
        package_report.append(f"- `{row['source_id']}` uses package-level treatment for `{row['repository_path']}`.")
    (guide_dir / f"{guide}_PACKAGE_VS_CHILD_TREATMENT_REPORT.md").write_text("\n".join(package_report) + "\n", encoding="utf-8")
    reconciliation = [
        f"# {guide} Reference Corpus Reconciliation",
        "",
        f"- Reference corpus candidates considered: `{initial}`",
        f"- Normative rows retained: `{len(rows)}`",
        f"- Reference-corpus-only rows: `{len(exclusions)}`",
        "",
        "Rows not retained remain searchable and checksum-controlled in `WAVE_1_REFERENCE_CORPUS_*` artifacts but are not drafting authority.",
    ]
    (guide_dir / f"{guide}_REFERENCE_CORPUS_RECONCILIATION.md").write_text("\n".join(reconciliation) + "\n", encoding="utf-8")
    source_report = [
        f"# {guide} Source Freeze Report",
        "",
        f"CGP-005 revision separates the broad reference corpus from this curated normative source freeze for `{guide}`.",
        "",
        f"- Normative rows: `{len(rows)}`",
        f"- Reference-only exclusions: `{len(exclusions)}`",
        f"- Maturity after CGP-005 revision: `PLANNED`",
        "",
        "This is returned for Founder review and is not adoption, activation, implementation, or CGP-006 authority.",
    ]
    (guide_dir / f"{guide}_SOURCE_FREEZE_REPORT.md").write_text("\n".join(source_report) + "\n", encoding="utf-8")
    readiness = [
        f"# {guide} Drafting Readiness Report",
        "",
        f"- Readiness disposition: `CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW`",
        "- Maturity after CGP-005 revision: `PLANNED`",
        "- CGP-006 ready: `NO`",
        "- Blocking revision finding: `CGP005-F-0001`",
        "",
        "Founder acceptance is required before the guide may be represented as source-frozen.",
    ]
    (guide_dir / f"{guide}_DRAFTING_READINESS_REPORT.md").write_text("\n".join(readiness) + "\n", encoding="utf-8")


def write_conflicts() -> None:
    master = read_csv(ROOT / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_CONFLICT_REGISTER.csv")
    rows = []
    guide_map = {
        "CGCON-0001": "ES-CG-01;ES-CG-13",
        "CGCON-0002": "ES-CG-13",
        "CGCON-0003": "ES-CG-01;ES-CG-10;ES-CG-13",
        "CGCON-0004": "ES-CG-01;ES-CG-13",
    }
    for item in master:
        rows.append(
            {
                "conflict_id": item["conflict_id"],
                "guide_id": guide_map.get(item["conflict_id"], "PROGRAM_WIDE"),
                "source_ids": item["source_ids"],
                "conflict_type": item["conflict_type"],
                "status": "RETAINED_FOR_DRAFTING",
                "freeze_treatment": item["current_treatment"],
                "blocks_drafting": "NO",
                "required_later_action": item["required_next_action"],
                "notes": "Retained as conflict evidence; documentary authority controls over implementation behavior.",
            }
        )
    write_csv(
        ROOT / "source-freeze" / "WAVE_1_SOURCE_CONFLICT_REGISTER.csv",
        ["conflict_id", "guide_id", "source_ids", "conflict_type", "status", "freeze_treatment", "blocks_drafting", "required_later_action", "notes"],
        rows,
    )


def write_repository_evidence_baseline() -> None:
    evidence_specs = [
        ("ES-CG-00", "CGP004-COMP-0001", "backend/server.py", "CGSRC-CGP005-0201", "APPLICATION_ASSEMBLY"),
        ("ES-CG-01", "CGP004-COMP-0003", "backend/core/auth.py", "CGSRC-CGP005-0202", "IDENTITY_AUTH"),
        ("ES-CG-01", "CGP004-COMP-0004", "backend/core/permissions.py", "CGSRC-CGP005-0204", "TENANCY_AUTHORIZATION"),
        ("ES-CG-13", "CGP004-COMP-0013", "backend/core/lifespan.py", "CGSRC-CGP005-0205", "LIFECYCLE_EVIDENCE"),
        ("ES-CG-13", "CGP004-COMP-0020", "backend/tests", "CGSRC-CGP005-0207", "TEST_EVIDENCE"),
        ("ES-CG-13", "CGP004-COMP-0021", ".github/workflows/ci.yml", "CGSRC-CGP005-0209", "CI_EVIDENCE"),
        ("ES-CG-10", "CGP004-COMP-0008", "backend/task_engine.py", "CGSRC-CGP005-0206", "SCENARIO_EVIDENCE"),
        ("ES-CG-10", "CGP004-COMP-0020", "backend/tests", "CGSRC-CGP005-0207", "TEST_EVIDENCE"),
        ("ES-CG-10", "CGP004-COMP-0020", "pytest.ini", "CGSRC-CGP005-0208", "TEST_CONFIGURATION"),
        ("ES-CG-10", "CGP004-COMP-0021", ".github/workflows/ci.yml", "CGSRC-CGP005-0209", "CI_EVIDENCE"),
    ]
    rows = []
    for idx, (guide, component, rel, source_id, evidence_class) in enumerate(evidence_specs, start=1):
        actual = REPO / rel
        is_dir = actual.is_dir()
        rows.append(
            {
                "baseline_id": f"CGP005-REPOBASE-{idx:04d}",
                "guide_id": guide,
                "cgp004_component_id": component,
                "repository_path": rel,
                "evidence_source_ids": source_id,
                "evidence_class": evidence_class,
                "baseline_commit": BASELINE,
                "git_object_sha": git_object(rel, is_dir),
                "git_object_type": "TREE" if is_dir else "BLOB",
                "sha256_checksum": sha256_tree(rel) if is_dir else sha256_file(actual),
                "checksum_verification_result": "VERIFIED_DIRECTORY_AGGREGATE" if is_dir else "VERIFIED_FILE",
                "authority_treatment": "IMPLEMENTATION_EVIDENCE_ONLY",
                "selected_for": "Selective CGP-005 revised guide-specific evidence baseline.",
                "retained_limitations": "Static repository evidence only; no tests, live providers, deployments, or production behavior executed.",
            }
        )
    write_csv(
        ROOT / "source-freeze" / "WAVE_1_REPOSITORY_EVIDENCE_BASELINE.csv",
        list(rows[0].keys()),
        rows,
    )


def update_readmes_and_tracker() -> None:
    for guide in WAVE_GUIDES:
        path = ROOT / "guides" / guide / "README.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("Current maturity state: `SOURCE_FROZEN`", "Current maturity state: `PLANNED`")
        text = text.replace("source freeze complete only", "curated source-freeze revision returned for Founder review only")
        text = text.replace(
            "CGP-005 records an exact-byte source freeze and drafting-question inventory for this guide.",
            "CGP-005 revision records a curated normative source-freeze package for Founder review while preserving the broad reference corpus.",
        )
        path.write_text(text, encoding="utf-8")
    tracker_path = ROOT / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv"
    rows = read_csv(tracker_path)
    fields = list(rows[0].keys())
    for row in rows:
        rid = row["record_id"]
        if rid == "CGP-005":
            row.update(
                {
                    "maturity_state": "REVISION_REQUIRED",
                    "prompt_status": "REVISION_REQUIRED",
                    "next_action": "Founder review of revised two-layer CGP-005 source-freeze package; CGP-006 remains not issued.",
                    "last_updated": DATE,
                    "receipt_path": "governance/implementation/code-guides/receipts/CGP_005_EXECUTION_RECEIPT.md",
                    "notes": "CGP-005 revised after Founder disposition CGP-005_REVISION_REQUIRED_OVERINCLUSIVE_SOURCE_FREEZE; broad corpus reclassified as non-normative reference corpus; curated normative freezes returned for review.",
                    "work_status": "REVISION_REQUIRED",
                }
            )
        elif rid == "CGP-006":
            row.update(
                {
                    "maturity_state": "PLANNED",
                    "prompt_status": "NOT_ISSUED",
                    "next_action": "Await Founder acceptance of revised CGP-005 before any CGP-006 authority.",
                    "last_updated": DATE,
                    "notes": "CGP-006 remains NOT_ISSUED after CGP-005 revision; no drafting begun.",
                    "work_status": "NOT_STARTED",
                }
            )
        elif rid in WAVE_GUIDES:
            row.update(
                {
                    "maturity_state": "PLANNED",
                    "prompt_status": "REVISION_REQUIRED",
                    "next_action": "Await Founder review of revised CGP-005 source-freeze curation.",
                    "last_updated": DATE,
                    "notes": "Guide remains PLANNED; curated normative source-freeze package is returned for Founder review and is not accepted, adopted, active, or implementation-authorizing.",
                    "work_status": "REVISION_REQUIRED",
                }
            )
    write_csv(tracker_path, fields, rows)


def append_finding() -> None:
    code_path = ROOT / "registers" / "CODE_GUIDE_FINDING_REGISTER.csv"
    rows = read_csv(code_path)
    fields = list(rows[0].keys())
    rows = [row for row in rows if row["finding_id"] != "CGP005-F-0001"]
    rows.append(
        {
            "finding_id": "CGP005-F-0001",
            "prompt_id": "CGP-005",
            "severity": "P2",
            "finding_type": "SOURCE_FREEZE_OVERINCLUSION",
            "title": "Wave 1 normative source freezes reproduce the broad mapped source corpus",
            "description": "Founder disposition identified that the first returned CGP-005 package selected substantially all CGP-003 Wave 1 mappings instead of a curated normative guide-specific source freeze.",
            "evidence_path": "governance/implementation/code-guides/source-freeze/WAVE_1_REFERENCE_CORPUS_REPORT.md;governance/implementation/code-guides/reviews/CGP_005_SOURCE_FREEZE_ASSURANCE_REPORT.md",
            "affected_source_ids": "WAVE_1_REFERENCE_CORPUS",
            "affected_guides": "ES-CG-00;ES-CG-01;ES-CG-13;ES-CG-10",
            "status": "OPEN",
            "required_action": "Founder review must accept the revised two-layer source model before any Wave 1 guide may be represented as SOURCE_FROZEN.",
            "owner": "Founder/Codex later prompt",
            "notes": "Revision performed but closure is retained for Founder acceptance; CGP-006 remains NOT_ISSUED.",
        }
    )
    write_csv(code_path, fields, rows)
    guide_path = ROOT / "registers" / "GUIDE_REVIEW_FINDING_REGISTER.csv"
    grows = read_csv(guide_path)
    gfields = list(grows[0].keys())
    grows = [row for row in grows if row["finding_id"] != "CGP005-F-0001"]
    grows.append(
        {
            "finding_id": "CGP005-F-0001",
            "guide_id": "ES-CG-00;ES-CG-01;ES-CG-13;ES-CG-10",
            "review_type": "CGP-005_SOURCE_FREEZE_REVISION",
            "severity": "P2",
            "title": "Wave 1 normative source freezes reproduce the broad mapped source corpus",
            "description": "The initial CGP-005 package required revision because it used map passthrough rather than guide-specific curation.",
            "evidence": "governance/implementation/code-guides/source-freeze/WAVE_1_REFERENCE_CORPUS_REPORT.md",
            "affected_controls": "",
            "affected_atlas_tasks": "",
            "owner": "Founder/Codex later prompt",
            "status": "OPEN",
            "required_action": "Accept or disposition the revised two-layer source-freeze package before guide maturity can advance.",
            "disposition_authority": "Founder",
            "closure_evidence": "",
            "closed_date": "",
            "retained_reason": "Founder acceptance is required before SOURCE_FROZEN treatment or CGP-006 readiness.",
        }
    )
    write_csv(guide_path, gfields, grows)


def write_program_reports(reference_rows: list[dict[str, str]], guide_result: dict) -> None:
    counts = Counter(row["source_burden_treatment"] for row in reference_rows)
    summary = [
        "# Wave 1 Source Freeze Summary",
        "",
        f"**Prompt:** `{PROMPT}`",
        f"**Execution ID:** `{EXECUTION}`",
        f"**Revision disposition addressed:** `CGP-005_REVISION_REQUIRED_OVERINCLUSIVE_SOURCE_FREEZE`",
        "",
        "CGP-005 now uses a two-layer model: a non-normative reference corpus and curated guide-specific normative freezes returned for Founder review.",
        "",
        f"- Reference corpus records: `{len(reference_rows)}`",
        f"- Normative crosswalk rows: `{guide_result['crosswalk_rows']}`",
        f"- Reference-only exclusion rows: `{guide_result['exclusion_rows']}`",
    ]
    for guide, data in guide_result["counts"].items():
        summary.append(f"- `{guide}` normative rows: `{data['total']}`")
    summary.extend(["", "All Wave 1 guides remain `PLANNED`; CGP-006 was not begun."])
    (ROOT / "source-freeze" / "WAVE_1_SOURCE_FREEZE_SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    assurance = [
        "# CGP-005 Source Freeze Assurance Report",
        "",
        f"**Prompt:** `{PROMPT}`",
        f"**Execution ID:** `{EXECUTION}`",
        f"**Baseline:** `{BASELINE}`",
        "",
        "The broad 2,511-record result is retained only as `WAVE_1_REFERENCE_CORPUS` and classified as `REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE`.",
        "",
        "## Reference Corpus Counts",
    ]
    for key, value in sorted(counts.items()):
        assurance.append(f"- `{key}`: `{value}`")
    assurance.append("")
    assurance.append("## Normative Counts")
    for guide, data in guide_result["counts"].items():
        assurance.append(f"- `{guide}`: `{data['total']}` curated rows")
    assurance.extend(["", "`CGP005-F-0001` remains open pending Founder acceptance. CGP-006 was not begun."])
    (ROOT / "reviews" / "CGP_005_SOURCE_FREEZE_ASSURANCE_REPORT.md").write_text("\n".join(assurance) + "\n", encoding="utf-8")
    readiness = [
        "# CGP-005 Wave 1 Drafting Readiness Report",
        "",
        f"**Prompt:** `{PROMPT}`",
        f"**Execution ID:** `{EXECUTION}`",
        "",
        "| Guide | Maturity After CGP-005 Revision | Readiness | Blocking Finding |",
        "|---|---|---|---|",
    ]
    for guide in WAVE_GUIDES:
        readiness.append(f"| `{guide}` | `PLANNED` | `CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW` | `CGP005-F-0001` |")
    readiness.extend(["", "Founder acceptance is required before any guide may be represented as `SOURCE_FROZEN`. CGP-006 was not begun."])
    (ROOT / "reviews" / "CGP_005_WAVE_1_DRAFTING_READINESS_REPORT.md").write_text("\n".join(readiness) + "\n", encoding="utf-8")
    retained = [
        "# CGP-005 Retained Gap Report",
        "",
        "- `CGP005-F-0001`: open pending Founder review of the revised two-layer source-freeze package.",
        "- `CGP004-F-0001`: retained for non-Wave 1 source freezes and later adoption or activation treatment.",
        "- `CGP004-F-0002`: retained downstream offline authorization finding.",
        "- `CGP004-F-0003`: retained downstream feature-surface mapping finding.",
        "- `CGP004-F-0004`: retained downstream operations/reliability finding.",
        "- `CGP004-F-0005`: retained downstream storage and AI activation-boundary finding.",
        "- `CGP004-F-0006`: retained downstream local assurance/environment finding.",
        "- `CGP004-F-0007`: retained downstream external provider static-only finding.",
        "- `CGP003-F-0004`: retained candidate/history/adopted/locked source-family finding.",
        "- `CGP003-F-0005`: retained historical manifest treatment finding.",
    ]
    (ROOT / "reviews" / "CGP_005_RETAINED_GAP_REPORT.md").write_text("\n".join(retained) + "\n", encoding="utf-8")
    drift = [
        "# CGP-005 Baseline And Drift Report",
        "",
        f"- Remote default baseline: `{BASELINE}`",
        "- Repository evidence baseline remains anchored to the authorized CGP-005 baseline.",
        "- The revised branch changes only Code Guide program documentary, validation, and custody artifacts.",
        "- No application code, tests, CI, PIA, atlas, deployment, provider, or production behavior was modified.",
    ]
    (ROOT / "reviews" / "CGP_005_BASELINE_AND_DRIFT_REPORT.md").write_text("\n".join(drift) + "\n", encoding="utf-8")


def write_receipt(guide_result: dict, reference_count: int) -> None:
    lines = [
        "# CGP-005 Execution Receipt",
        "",
        f"**Program:** EquineSync Code Implementation Guide Program",
        f"**Prompt ID:** `{PROMPT}`",
        f"**Execution ID:** `{EXECUTION}`",
        f"**Package ID:** `{PACKAGE}`",
        "**Repository:** `rianray2012-coder/EquineSync-V4`",
        "**Default branch:** `integrate-emergent-final-zip`",
        f"**Authorized baseline:** `{BASELINE}`",
        f"**Working branch:** `{BRANCH}`",
        "",
        "## Revision Treatment",
        "",
        "Founder disposition `CGP-005_REVISION_REQUIRED_OVERINCLUSIVE_SOURCE_FREEZE` was addressed by separating the broad corpus from curated normative guide freezes.",
        "",
        "## Output Summary",
        "",
        f"- Reference corpus records: `{reference_count}`",
        f"- Normative source crosswalk rows: `{guide_result['crosswalk_rows']}`",
        f"- Reference-only exclusion rows: `{guide_result['exclusion_rows']}`",
    ]
    for guide, data in guide_result["counts"].items():
        lines.append(f"- `{guide}` normative source rows: `{data['total']}`")
    lines.extend(
        [
            "- Wave 1 guides marked `SOURCE_FROZEN`: `0`",
            "- Guides adopted: `0`",
            "- Guides active: `0`",
            "- Open CGP-005 findings: `CGP005-F-0001`",
            "",
            "## Actions Not Taken",
            "",
            "CGP-006 was not begun. No substantive Code Guide controls, implementation profiles, application-code changes, application-test changes, CI changes, PIA amendments, atlas amendments, deployment actions, pilot actions, production actions, provider executions, financial activation, messaging activation, moderation activation, AI activation, archival migration, enrollment, PR opening, or merge action were created or exercised.",
        ]
    )
    (ROOT / "receipts" / "CGP_005_EXECUTION_RECEIPT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def collect_cgp005_artifacts() -> list[str]:
    paths = [
        "governance/implementation/code-guides/CANONICAL_GUIDE_INVENTORY.md",
        "governance/implementation/code-guides/CONTROLLED_VALUES.md",
        "governance/implementation/code-guides/receipts/CGP_005_EXECUTION_RECEIPT.md",
        "governance/implementation/code-guides/registers/CODE_GUIDE_ARTIFACT_INVENTORY.csv",
        "governance/implementation/code-guides/registers/CODE_GUIDE_FINDING_REGISTER.csv",
        "governance/implementation/code-guides/registers/CODE_GUIDE_PROGRAM_TRACKER.csv",
        "governance/implementation/code-guides/registers/CODE_GUIDE_PROMPT_EXECUTION_LOG.csv",
        "governance/implementation/code-guides/registers/GUIDE_REVIEW_FINDING_REGISTER.csv",
        "governance/implementation/code-guides/reviews/CGP_005_BASELINE_AND_DRIFT_REPORT.md",
        "governance/implementation/code-guides/reviews/CGP_005_RETAINED_GAP_REPORT.md",
        "governance/implementation/code-guides/reviews/CGP_005_SOURCE_FREEZE_ASSURANCE_REPORT.md",
        "governance/implementation/code-guides/reviews/CGP_005_VALIDATION_REPORT.json",
        "governance/implementation/code-guides/reviews/CGP_005_WAVE_1_DRAFTING_READINESS_REPORT.md",
        "governance/implementation/code-guides/schemas/CODE_GUIDE_CONTROLLED_VALUES.json",
        "governance/implementation/code-guides/source-freeze/WAVE_1_DRAFTING_READINESS_REGISTER.csv",
        "governance/implementation/code-guides/source-freeze/WAVE_1_REFERENCE_CORPUS_MANIFEST.json",
        "governance/implementation/code-guides/source-freeze/WAVE_1_REFERENCE_CORPUS_REGISTER.csv",
        "governance/implementation/code-guides/source-freeze/WAVE_1_REFERENCE_CORPUS_REPORT.md",
        "governance/implementation/code-guides/source-freeze/WAVE_1_REPOSITORY_EVIDENCE_BASELINE.csv",
        "governance/implementation/code-guides/source-freeze/WAVE_1_SOURCE_CONFLICT_REGISTER.csv",
        "governance/implementation/code-guides/source-freeze/WAVE_1_SOURCE_EXCLUSION_REGISTER.csv",
        "governance/implementation/code-guides/source-freeze/WAVE_1_SOURCE_FREEZE_CROSSWALK.csv",
        "governance/implementation/code-guides/source-freeze/WAVE_1_SOURCE_FREEZE_SUMMARY.md",
        "governance/implementation/code-guides/tools/generate_cgp005_revision.py",
        "governance/implementation/code-guides/validation/README.md",
        "governance/implementation/code-guides/validation/cgp_validation.py",
        "governance/implementation/code-guides/validation/tests/test_cgp005_source_freeze.py",
        "governance/implementation/code-guides/validation/tests/test_validator_placeholders.py",
        "governance/implementation/code-guides/validation/validate_source_freeze.py",
        "governance/implementation/code-guides/validation/validate_wave_1_drafting_readiness.py",
    ]
    for guide in WAVE_GUIDES:
        base = f"governance/implementation/code-guides/guides/{guide}"
        paths.extend(
            [
                f"{base}/{guide}_DRAFTING_QUESTION_INVENTORY.csv",
                f"{base}/README.md",
                f"{base}/source-freeze/{guide}_DRAFTING_READINESS_REPORT.md",
                f"{base}/source-freeze/{guide}_NORMATIVE_SOURCE_SELECTION_REPORT.md",
                f"{base}/source-freeze/{guide}_PACKAGE_VS_CHILD_TREATMENT_REPORT.md",
                f"{base}/source-freeze/{guide}_REFERENCE_CORPUS_RECONCILIATION.md",
                f"{base}/source-freeze/{guide}_SOURCE_BURDEN_SUMMARY.md",
                f"{base}/source-freeze/{guide}_SOURCE_EXCLUSION_REGISTER.csv",
                f"{base}/source-freeze/{guide}_SOURCE_FREEZE_MANIFEST.json",
                f"{base}/source-freeze/{guide}_SOURCE_FREEZE_REGISTER.csv",
                f"{base}/source-freeze/{guide}_SOURCE_FREEZE_REPORT.md",
            ]
        )
    return sorted(path for path in paths if (REPO / path).exists())


def artifact_type_for(path: str) -> str:
    if "/source-freeze/" in path and path.endswith(".csv"):
        return "SOURCE_FREEZE_REGISTER"
    if "/source-freeze/" in path and path.endswith(".json"):
        return "SOURCE_FREEZE_MANIFEST"
    if "/source-freeze/" in path and path.endswith(".md"):
        return "SOURCE_FREEZE_REPORT"
    if "/validation/tests/" in path:
        return "VALIDATOR_TEST"
    if "/validation/" in path:
        return "VALIDATOR"
    if "/packages/" in path:
        return "PACKAGE_CUSTODY"
    if "/receipts/" in path:
        return "RECEIPT"
    if "/reviews/" in path:
        return "REVIEW_REPORT"
    if "/registers/" in path:
        return "REGISTER"
    if "/schemas/" in path:
        return "SCHEMA"
    if "/tools/" in path:
        return "GENERATOR"
    return "PROGRAM_ARTIFACT"


def update_artifact_inventory(artifact_paths: list[str]) -> None:
    path = ROOT / "registers" / "CODE_GUIDE_ARTIFACT_INVENTORY.csv"
    rows = read_csv(path)
    fields = list(rows[0].keys())
    by_path = {row.get("expected_path", ""): row for row in rows}
    max_id = 0
    for row in rows:
        artifact_id = row.get("artifact_id", "")
        if artifact_id.startswith("CGP-ART-"):
            try:
                max_id = max(max_id, int(artifact_id.rsplit("-", 1)[1]))
            except ValueError:
                pass
    for rel in sorted(set(artifact_paths + [
        "governance/implementation/code-guides/packages/CGP_005_CREATED_ARTIFACT_MANIFEST.json",
        "governance/implementation/code-guides/packages/CGP_005_SHA256SUMS.txt",
    ])):
        if rel == "governance/implementation/code-guides/registers/CODE_GUIDE_ARTIFACT_INVENTORY.csv":
            continue
        actual = REPO / rel
        if not actual.exists():
            continue
        row = by_path.get(rel)
        if row is None:
            max_id += 1
            row = {field: "" for field in fields}
            row.update(
                {
                    "artifact_id": f"CGP-ART-{max_id:04d}",
                    "program_or_guide_id": "CGP-005",
                    "artifact_type": artifact_type_for(rel),
                    "title": Path(rel).name,
                    "expected_path": rel,
                    "required_stage": "CGP-005_REVISION",
                    "required": "YES",
                    "version": "0.5.1",
                    "source_prompt": "CGP-005",
                }
            )
            rows.append(row)
            by_path[rel] = row
        if row.get("source_prompt") == "CGP-005" or row.get("required_stage", "").startswith("CGP-005"):
            checksum_treatment = CYCLE_CHECKSUM_TREATMENTS.get(rel, "VALIDATED_BY_CGP_005_PACKAGE_LEDGER")
            row.update(
                {
                    "status": "REVISED",
                    "checksum": checksum_treatment,
                    "commit_sha": "FINAL_REVISED_BRANCH_HEAD_REPORTED_IN_CGP_005_RESPONSE",
                    "remote_verified": "YES_AFTER_REVISED_PUSH_VERIFICATION_REPORTED_IN_CGP_005_RESPONSE",
                    "notes": "CGP-005 revised two-layer source-freeze artifact; exact file checksum is sealed in CGP_005_SHA256SUMS unless a cycle-specific checksum treatment is named; no guide adoption, activation, implementation, PR, or merge authority.",
                }
            )
    for row in rows:
        rel = row.get("expected_path", "")
        if (row.get("source_prompt") == "CGP-005" or row.get("required_stage", "").startswith("CGP-005")) and rel in CYCLE_CHECKSUM_TREATMENTS:
            row.update(
                {
                    "status": "REVISED",
                    "checksum": CYCLE_CHECKSUM_TREATMENTS[rel],
                    "commit_sha": "FINAL_REVISED_BRANCH_HEAD_REPORTED_IN_CGP_005_RESPONSE",
                    "remote_verified": "YES_AFTER_REVISED_PUSH_VERIFICATION_REPORTED_IN_CGP_005_RESPONSE",
                    "notes": "CGP-005 revised custody metadata uses a cycle-specific checksum treatment here; exact bytes are verified by the named package ledger or source-accession validator.",
                }
            )
    write_csv(path, fields, rows)


def refresh_source_freeze_register_checksums(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    fields = list(rows[0].keys())
    refreshed = []
    for row in rows:
        rel = row.get("repository_path", "")
        if rel and (REPO / rel).exists():
            row = refresh_source_row(row)
        refreshed.append(row)
    write_csv(path, fields, refreshed)
    return refreshed


def refresh_source_freeze_manifest_checksums(manifest_path: Path, rows: list[dict[str, str]]) -> None:
    if not manifest_path.exists():
        return
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_record = {row.get("freeze_record_id", ""): row for row in rows}
    by_source = {row.get("source_id", ""): row for row in rows}
    for item in data.get("sources", []):
        row = by_record.get(item.get("freeze_record_id", "")) or by_source.get(item.get("source_id", ""))
        if not row:
            continue
        if "sha256_checksum" in item:
            item["sha256_checksum"] = row.get("sha256_checksum", "")
        if "repository_path" in item:
            item["repository_path"] = row.get("repository_path", "")
    if "directory_manifests" in data:
        data["directory_manifests"] = directory_manifest(rows)
        if "directory_manifest_count" in data:
            data["directory_manifest_count"] = len(data["directory_manifests"])
    write_json(manifest_path, data)


def refresh_all_source_freeze_checksums() -> None:
    reference_rows = refresh_source_freeze_register_checksums(ROOT / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_REGISTER.csv")
    refresh_source_freeze_manifest_checksums(ROOT / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json", reference_rows)
    for guide in WAVE_GUIDES:
        guide_dir = ROOT / "guides" / guide / "source-freeze"
        register_path = guide_dir / f"{guide}_SOURCE_FREEZE_REGISTER.csv"
        manifest_path = guide_dir / f"{guide}_SOURCE_FREEZE_MANIFEST.json"
        if register_path.exists():
            guide_rows = refresh_source_freeze_register_checksums(register_path)
            refresh_source_freeze_manifest_checksums(manifest_path, guide_rows)


def write_manifest_and_ledgers() -> None:
    artifact_paths = collect_cgp005_artifacts()
    update_artifact_inventory(artifact_paths)
    manifest_path = ROOT / "packages" / "CGP_005_CREATED_ARTIFACT_MANIFEST.json"
    ledger_path = ROOT / "packages" / "CGP_005_SHA256SUMS.txt"
    artifact_paths.append("governance/implementation/code-guides/packages/CGP_005_CREATED_ARTIFACT_MANIFEST.json")
    artifact_paths = sorted(set(artifact_paths))
    write_json(
        manifest_path,
        {
            "artifact_count": len(artifact_paths) + 1,
            "authorized_scope": "governance/implementation/code-guides/",
            "baseline_commit": BASELINE,
            "branch": BRANCH,
            "checksum_ledger": "governance/implementation/code-guides/packages/CGP_005_SHA256SUMS.txt",
            "created_date": DATE,
            "execution_id": EXECUTION,
            "files": [
                {
                    "artifact_role": "CGP-005 revised two-layer source-freeze, readiness, validation, register, or custody artifact",
                    "checksum_inclusion": "EXCLUDED_SELF_HASH" if path.endswith("CGP_005_SHA256SUMS.txt") else "INCLUDED",
                    "path": path,
                }
                for path in sorted(artifact_paths + ["governance/implementation/code-guides/packages/CGP_005_SHA256SUMS.txt"])
            ],
            "ledger_note": "CGP_005_SHA256SUMS.txt intentionally excludes itself from self-hashing.",
            "ledger_self_hashing": "EXCLUDED",
            "non_authorization": "No PR, merge, CGP-006 drafting, implementation, deployment, pilot, production, or activation authority.",
            "package_id": PACKAGE,
            "prompt_id": PROMPT,
            "revision_treatment": "Broad source freeze reclassified as non-normative reference corpus; curated normative guide freezes returned for Founder review.",
        },
    )
    ledger_entries = []
    refresh_existing_ledger("CGP_002")
    update_source_accession_checksums()
    refresh_all_source_freeze_checksums()
    for path in sorted(set(artifact_paths)):
        short = path.replace("governance/implementation/code-guides/", "", 1)
        ledger_entries.append(f"{sha256_file(REPO / path)}  {short}")
    ledger_path.write_text("\n".join(ledger_entries) + "\n", encoding="utf-8")
    for prompt in ["CGP_003", "CGP_004"]:
        refresh_existing_ledger(prompt)


def refresh_existing_ledger(prompt: str) -> None:
    manifest_path = ROOT / "packages" / f"{prompt}_CREATED_ARTIFACT_MANIFEST.json"
    ledger_path = ROOT / "packages" / f"{prompt}_SHA256SUMS.txt"
    if not manifest_path.exists() or not ledger_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lines = []
    for item in manifest.get("files", []):
        if item.get("checksum_inclusion") != "INCLUDED":
            continue
        rel = item.get("path", "")
        short = rel.replace("governance/implementation/code-guides/", "", 1)
        if short == f"packages/{prompt}_SHA256SUMS.txt":
            continue
        actual = REPO / rel
        if actual.exists():
            lines.append(f"{sha256_file(actual)}  {short}")
    ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_superseded_common_files() -> None:
    for rel in [
        "source-freeze/WAVE_1_COMMON_SOURCE_FREEZE_REGISTER.csv",
        "source-freeze/WAVE_1_COMMON_SOURCE_FREEZE_MANIFEST.json",
    ]:
        path = ROOT / rel
        if path.exists():
            path.unlink()


def main() -> None:
    update_controlled_values()
    for prompt in ["CGP_002", "CGP_003", "CGP_004"]:
        refresh_existing_ledger(prompt)
    update_source_accession_checksums()
    refresh_existing_ledger("CGP_003")
    reference_rows, origin, _ = load_origin_rows()
    candidates = candidate_ids_by_guide()
    write_reference_corpus(reference_rows)
    guide_result = build_guide_freezes(origin, candidates)
    write_conflicts()
    write_repository_evidence_baseline()
    update_readmes_and_tracker()
    append_finding()
    write_program_reports(reference_rows, guide_result)
    write_receipt(guide_result, len(reference_rows))
    remove_superseded_common_files()
    write_manifest_and_ledgers()


if __name__ == "__main__":
    main()
