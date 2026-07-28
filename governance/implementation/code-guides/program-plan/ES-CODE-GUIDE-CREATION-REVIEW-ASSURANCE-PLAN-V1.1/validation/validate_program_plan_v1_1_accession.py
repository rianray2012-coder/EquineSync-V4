#!/usr/bin/env python3
"""Validate the Code Guide Program Plan V1.1 accession package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[6]
PACKAGE_REL = PACKAGE_ROOT.relative_to(REPO_ROOT).as_posix()

PROGRAM_ID = "ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1"
EXPECTED_SOURCE = "ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1.md"
EXPECTED_SOURCE_SHA256 = "9aa8cb29848ccf5b75a65320616a1196060589372bb0de09266fd32f3a9efd35"
EXPECTED_SOURCE_SIZE = 54852
EXPECTED_BASE = "2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94"

REQUIRED_FILES = {
    ".gitattributes",
    EXPECTED_SOURCE,
    "FOUNDER_APPROVAL_AND_RATIFICATION_DISPOSITION.md",
    "PROGRAM_DOCUMENT_OVERVIEW.md",
    "V1_0_TO_V1_1_CHANGE_AND_STRENGTHENING_SUMMARY.md",
    "AUTHORITY_AND_SUPERSESSION_ANALYSIS.md",
    "PRIOR_CGP_LIMITED_RATIFICATION_ANALYSIS.md",
    "SOURCE_REGISTER.md",
    "SOURCE_FREEZE_MANIFEST.json",
    "SOURCE_SHA256SUMS.txt",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "VALIDATION_REPORT.md",
    "REVIEW_DISPOSITION.md",
    "PROTECTED_INTEGRATION_PLAN.md",
    "validation/validate_program_plan_v1_1_accession.py",
    "tests/test_validate_program_plan_v1_1_accession.py",
}

REQUIRED_TOKENS = {
    "FOUNDER_APPROVAL_AND_RATIFICATION_DISPOSITION.md": [
        "FOUNDER_APPROVED_CONTROLLING_DOCUMENTARY_PROGRAM_PLAN",
        "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED_BY_PLAN_APPROVAL_ALONE",
        "IMPLEMENTATION_NOT_AUTHORIZED",
        "GUIDE_ACTIVATION_NOT_AUTHORIZED",
        "DEPLOYMENT_NOT_AUTHORIZED",
        "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
        "FIRST_USER_ENROLLMENT_NOT_AUTHORIZED",
    ],
    "AUTHORITY_AND_SUPERSESSION_ANALYSIS.md": [
        "DOCUMENTARY_PROGRAM_PLAN_ACCESSION_CUSTODY_AND_RECONCILIATION_ONLY",
        "HISTORICAL_SOURCE_NOT_LOCATED_IN_CANONICAL_REPOSITORY",
    ],
    "PRIOR_CGP_LIMITED_RATIFICATION_ANALYSIS.md": [
        "CGP005-TA-APP-GAP-0004",
        "CGP006-CLF-0001",
        "CGP006-CLF-0005",
        "All guide bytes remain unchanged.",
    ],
    "PROGRAM_DOCUMENT_OVERVIEW.md": [
        "f94c26188e8d35c413b366135df12057b58c2d7d",
        "PR #44 is preserved as open, draft, unmerged, and unmodified",
    ],
}

ALLOWED_CHANGED_PREFIXES = (
    f"{PACKAGE_REL}/",
    "governance/implementation/code-guides/README.md",
    "governance/implementation/code-guides/PROGRAM_STATUS.md",
    "governance/implementation/code-guides/registers/CODE_GUIDE_VERSION_REGISTER.csv",
    "governance/implementation/code-guides/registers/GUIDE_SUPERSESSION_REGISTER.csv",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_required_files() -> None:
    missing = [name for name in sorted(REQUIRED_FILES) if not (PACKAGE_ROOT / name).is_file()]
    if missing:
        fail(f"missing required package files: {missing}")


def validate_source_identity() -> None:
    source = PACKAGE_ROOT / EXPECTED_SOURCE
    data = source.read_bytes()
    if len(data) != EXPECTED_SOURCE_SIZE:
        fail(f"source byte length mismatch: {len(data)}")
    actual = hashlib.sha256(data).hexdigest()
    if actual != EXPECTED_SOURCE_SHA256:
        fail(f"source hash mismatch: {actual}")
    if PROGRAM_ID.encode("utf-8") not in data:
        fail("program id missing from source bytes")
    if b"FOUNDER_APPROVAL_CANDIDATE" not in data:
        fail("internal pre-approval status field was not preserved")


def validate_json_manifests() -> None:
    source_freeze = json.loads((PACKAGE_ROOT / "SOURCE_FREEZE_MANIFEST.json").read_text())
    if source_freeze["program_id"] != PROGRAM_ID:
        fail("source freeze manifest program id mismatch")
    if source_freeze["approved_source"]["sha256"] != EXPECTED_SOURCE_SHA256:
        fail("source freeze manifest source hash mismatch")
    if source_freeze["approved_source"]["byte_length"] != EXPECTED_SOURCE_SIZE:
        fail("source freeze manifest source size mismatch")
    if source_freeze["historical_v1_0_treatment"] != "HISTORICAL_SOURCE_NOT_LOCATED_IN_CANONICAL_REPOSITORY":
        fail("historical treatment mismatch")

    package_manifest = json.loads((PACKAGE_ROOT / "PACKAGE_MANIFEST.json").read_text())
    paths = {entry["path"] for entry in package_manifest["files"]}
    # The checksum ledger covers PACKAGE_MANIFEST.json. The package manifest
    # intentionally excludes its own final hash to avoid recursive mutation.
    expected = {
        f"{PACKAGE_REL}/{name}"
        for name in REQUIRED_FILES
        if name not in {"CHECKSUM_MANIFEST.sha256", "PACKAGE_MANIFEST.json"}
    }
    if not expected.issubset(paths):
        fail(f"package manifest missing paths: {sorted(expected - paths)}")
    if package_manifest["directive_id"] != "CGP_006_CODE_GUIDE_PROGRAM_PLAN_V1_1_PROTECTED_ACCESSION_CUSTODY_AND_PR_44_RECONCILIATION_DIRECTIVE_V1_0_0":
        fail("directive id mismatch")


def validate_checksum_manifest() -> None:
    manifest_path = PACKAGE_ROOT / "CHECKSUM_MANIFEST.sha256"
    recorded: dict[str, str] = {}
    for line in manifest_path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        recorded[rel] = digest

    expected_paths = {
        f"{PACKAGE_REL}/{name}"
        for name in REQUIRED_FILES
        if name != "CHECKSUM_MANIFEST.sha256"
    }
    if set(recorded) != expected_paths:
        fail(f"checksum manifest path mismatch: missing={sorted(expected_paths - set(recorded))} extra={sorted(set(recorded) - expected_paths)}")
    for rel, digest in sorted(recorded.items()):
        actual = sha256(REPO_ROOT / rel)
        if actual != digest:
            fail(f"checksum mismatch for {rel}: {actual} != {digest}")

    source_sums = (PACKAGE_ROOT / "SOURCE_SHA256SUMS.txt").read_text().splitlines()
    expected_line = f"{EXPECTED_SOURCE_SHA256}  {EXPECTED_SOURCE}"
    if expected_line not in source_sums:
        fail("source sha256sum entry missing")


def validate_required_tokens() -> None:
    for rel, tokens in REQUIRED_TOKENS.items():
        text = (PACKAGE_ROOT / rel).read_text()
        for token in tokens:
            if token not in text:
                fail(f"{rel} missing token {token}")


def validate_program_state_preservation() -> None:
    tracker_path = REPO_ROOT / "governance/implementation/code-guides/registers/CODE_GUIDE_PROGRAM_TRACKER.csv"
    with tracker_path.open(newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["record_type"] == "GUIDE"]
    if len(rows) != 14:
        fail(f"expected 14 guide rows, found {len(rows)}")
    for row in rows:
        if row["adoption_state"] != "NOT_ADOPTED":
            fail(f"guide adoption state changed: {row}")
        if row["work_status"] not in {"SOURCE_FROZEN", "NOT_STARTED"}:
            fail(f"unexpected guide work status: {row}")
        if row["guide_id"] in {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"}:
            if row["maturity_state"] != "SOURCE_FROZEN" or row["accession_state"] != "NOT_ACCESSIONED":
                fail(f"wave 1 guide state changed: {row}")
        elif row["maturity_state"] != "PLANNED" or row["accession_state"] != "NOT_ACCESSIONED":
            fail(f"later-wave guide state changed: {row}")


def validate_changed_scope() -> None:
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", f"{EXPECTED_BASE}...HEAD"],
            cwd=REPO_ROOT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        fail(f"git diff scope check failed: {exc}")
    changed = [line for line in output.splitlines() if line]
    if not changed:
        return
    forbidden = [
        path
        for path in changed
        if not any(path == allowed or path.startswith(allowed) for allowed in ALLOWED_CHANGED_PREFIXES)
    ]
    if forbidden:
        fail(f"forbidden changed paths: {forbidden}")


def main() -> int:
    checks = [
        validate_required_files,
        validate_source_identity,
        validate_json_manifests,
        validate_checksum_manifest,
        validate_required_tokens,
        validate_program_state_preservation,
        validate_changed_scope,
    ]
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print("PASS CODE_GUIDE_PROGRAM_PLAN_V1_1_ACCESSION_PACKAGE")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
