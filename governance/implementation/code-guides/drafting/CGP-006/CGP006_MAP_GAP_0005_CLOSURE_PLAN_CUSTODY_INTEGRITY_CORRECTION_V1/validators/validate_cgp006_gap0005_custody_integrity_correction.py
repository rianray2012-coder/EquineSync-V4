#!/usr/bin/env python3
"""Validate CGP-006 GAP-0005 custody integrity correction package."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

PACKAGE_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_V1")
ACCESSION_VALIDATOR = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1/validators/validate_cgp006_gap0005_closure_plan_accession.py")
CUSTODY_VALIDATOR = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_POST_MERGE_CUSTODY/validators/validate_cgp006_gap0005_closure_plan_custody.py")
PROGRAM_STATUS = Path("governance/implementation/code-guides/PROGRAM_STATUS.md")
ZIP_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1/APPROVED_SOURCE/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_2026_08_01.zip")
EXPECTED_ZIP_SHA = "56cec940bef67ca1a6932428398fdde7b3f7e78a9aee9f2b2f8e84b47ea49b95"
EXPECTED_ZIP_BYTES = 117450
REQUIRED_FILES = {
    "README.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "CUSTODY_INTEGRITY_DEFECT_AND_CORRECTION_RECORD.md",
    "MISSING_APPROVED_ZIP_CUSTODY_FINDING.md",
    "HISTORICAL_VALIDATOR_AND_MANIFEST_IDENTITY_RECORD.json",
    "BUGBOT_FINDING_DISPOSITION_MATRIX.csv",
    "APPROVED_ZIP_GIT_OBJECT_CUSTODY_RECORD.json",
    "ACCESSION_VALIDATOR_CORRECTION_RECORD.md",
    "CUSTODY_VALIDATOR_CORRECTION_RECORD.md",
    "NEGATIVE_TEST_MATRIX.csv",
    "AUTHORIZED_PATH_REPORT.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "VALIDATION_REPORT.md",
    "validators/validate_cgp006_gap0005_custody_integrity_correction.py",
    "tests/test_cgp006_gap0005_custody_integrity_correction.py",
}
SECRET_RE = re.compile(r"(sk_live_[A-Za-z0-9_]+|sk_test_[A-Za-z0-9_]+|rk_live_[A-Za-z0-9_]+|rk_test_[A-Za-z0-9_]+|whsec_[A-Za-z0-9_]+|mongodb(?:\+srv)?://|JWT_SECRET\s*=|STRIPE_SECRET_KEY\s*=.+|STRIPE_API_KEY\s*=.+)", re.IGNORECASE)
CONFLICT_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
TEXT_SUFFIXES = {".md", ".py", ".json", ".csv", ".sha256", ""}
BOUNDARY_TOKENS = [
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_FOUNDER_APPROVAL_REMAINS_VALID",
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_IN_PROGRESS",
    "CGP006_MAP_GAP_0005_PRIOR_CUSTODY_COMPLETION_RELIANCE_SUSPENDED",
    "CGP006_MAP_GAP_0005_PROVIDER_ASSURANCE_PHASE_0_BLOCKED",
    "CGP006_MAP_GAP_0005_REMAINS_OPEN",
    "NO_STRIPE_API_CALL_OCCURRED",
    "NO_STRIPE_SANDBOX_MUTATION_OCCURRED",
    "NO_LIVE_STRIPE_ACCESS_OCCURRED",
    "NO_STRIPE_SECRET_OR_OBJECT_USED",
    "NO_PRODUCT_CODE_CHANGED",
    "NO_SCHEMA_OR_MIGRATION_CHANGED",
    "PR_69_NOT_MODIFIED_OR_MERGED",
    "PR_70_NOT_MODIFIED_OR_MERGED",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[7]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(root: Path, *args: str, check: bool = True) -> str:
    cp = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        raise AssertionError(f"git command failed: {' '.join(args)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
    return cp.stdout.rstrip("\n")


def git_object_bytes(root: Path, rel: Path) -> bytes:
    rel_text = rel.as_posix()
    run_git(root, "ls-files", "--error-unmatch", rel_text)
    run_git(root, "cat-file", "-e", f"HEAD:{rel_text}")
    return subprocess.check_output(["git", "show", f"HEAD:{rel_text}"], cwd=root)


def load_validator(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_files(package: Path) -> set[str]:
    return {
        str(path.relative_to(package))
        for path in package.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }


def validate_manifest(package: Path, found: set[str]) -> None:
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != "CGP006-MAP-GAP-0005-CLOSURE-PLAN-CUSTODY-INTEGRITY-CORRECTION-V1":
        raise AssertionError("package manifest ID mismatch")
    for row in manifest.get("files", []):
        path = package / row["path"]
        if not path.is_file():
            raise AssertionError(f"manifest file missing: {row['path']}")
        data = path.read_bytes()
        if sha256_bytes(data) != row["sha256"] or len(data) != row["byte_length"]:
            raise AssertionError(f"manifest identity mismatch: {row['path']}")
    seen = set()
    for raw in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, rel = raw.split(maxsplit=1)
        path = package / rel
        if not path.is_file():
            raise AssertionError(f"checksum file missing: {rel}")
        if sha256_bytes(path.read_bytes()) != digest:
            raise AssertionError(f"checksum mismatch: {rel}")
        seen.add(rel)
    if seen != found - {"CHECKSUM_MANIFEST.sha256"}:
        raise AssertionError("checksum manifest inventory mismatch")


def validate() -> dict[str, object]:
    root = repo_root()
    package = root / PACKAGE_PATH
    found = package_files(package)
    missing = sorted(REQUIRED_FILES - found)
    if missing:
        raise AssertionError(f"missing correction package files: {missing}")
    for rel in sorted(found):
        path = package / rel
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as fh:
                list(csv.reader(fh))
        if path.suffix in TEXT_SUFFIXES:
            data = path.read_text(encoding="utf-8")
            if SECRET_RE.search(data):
                raise AssertionError(f"secret-like value found: {rel}")
            if CONFLICT_RE.search(data):
                raise AssertionError(f"conflict marker found: {rel}")
    text = "\n".join((package / rel).read_text(encoding="utf-8") for rel in found if (package / rel).suffix in TEXT_SUFFIXES)
    text += "\n" + (root / PROGRAM_STATUS).read_text(encoding="utf-8")
    for token in BOUNDARY_TOKENS:
        if token not in text:
            raise AssertionError(f"boundary token missing: {token}")
    zip_data = git_object_bytes(root, ZIP_PATH)
    if sha256_bytes(zip_data) != EXPECTED_ZIP_SHA or len(zip_data) != EXPECTED_ZIP_BYTES:
        raise AssertionError("approved ZIP Git object identity mismatch")
    accession_result = load_validator(root / ACCESSION_VALIDATOR).validate()
    custody_result = load_validator(root / CUSTODY_VALIDATOR).validate()
    validate_manifest(package, found)
    return {
        "status": "PASS",
        "package_files": len(found),
        "approved_zip_git_sha256": EXPECTED_ZIP_SHA,
        "approved_zip_git_bytes": EXPECTED_ZIP_BYTES,
        "accession_status": accession_result.get("status", "PASS") if isinstance(accession_result, dict) else "PASS",
        "custody_status": custody_result.get("status", "PASS") if isinstance(custody_result, dict) else "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
