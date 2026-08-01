#!/usr/bin/env python3
"""Validate CGP-006 GAP-0005 post-correction custody refresh package."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

PACKAGE_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2")
RECEIPT_PATH = Path("governance/implementation/code-guides/receipts/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2_RECEIPT.md")
PROGRAM_STATUS = Path("governance/implementation/code-guides/PROGRAM_STATUS.md")
ACCESSION_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1")
CUSTODY_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_POST_MERGE_CUSTODY")
CORRECTION_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_V1")
ACCESSION_VALIDATOR = ACCESSION_PATH / "validators/validate_cgp006_gap0005_closure_plan_accession.py"
CUSTODY_VALIDATOR = CUSTODY_PATH / "validators/validate_cgp006_gap0005_closure_plan_custody.py"
CORRECTION_VALIDATOR = CORRECTION_PATH / "validators/validate_cgp006_gap0005_custody_integrity_correction.py"
ZIP_PATH = ACCESSION_PATH / "APPROVED_SOURCE/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_2026_08_01.zip"
EXPECTED_ZIP_SHA = "56cec940bef67ca1a6932428398fdde7b3f7e78a9aee9f2b2f8e84b47ea49b95"
EXPECTED_ZIP_BYTES = 117450
STARTING_PROTECTED_HEAD = "0863d3f58a1e3eaffbfd0c9778272c207d43c471"
CORRECTION_HEAD = "7eb248ff6ec51d5d345f30dade02c6076ea130a2"
CORRECTION_MERGE = "099abfbc27c77146b444048326d00fb3a5a7eb5f"
PACKAGE_ID = "CGP006-MAP-GAP-0005-CLOSURE-PLAN-POST-CORRECTION-CUSTODY-REFRESH-V2"
REQUIRED_FILES = {
    "README.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "CORRECTIVE_PR_MERGE_RECEIPT.md",
    "CLEAN_DETACHED_CHECKOUT_RECORD.json",
    "APPROVED_ZIP_PROTECTED_GIT_OBJECT_RECORD.json",
    "ACCESSION_VALIDATION_REFRESH_REPORT.md",
    "CUSTODY_VALIDATION_REFRESH_REPORT.md",
    "BOUNDARY_TOKEN_LOCATION_MATRIX.csv",
    "PLACEHOLDER_REJECTION_VALIDATION_REPORT.md",
    "BUGBOT_FINDING_FINAL_DISPOSITION_MATRIX.csv",
    "CURRENT_STATUS_RECONCILIATION.md",
    "AUTHORIZED_PATH_REPORT.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "VALIDATION_REPORT.md",
    "validators/validate_cgp006_gap0005_post_correction_custody_refresh.py",
    "tests/test_cgp006_gap0005_post_correction_custody_refresh.py",
}
PROHIBITED_PLACEHOLDERS = {
    "CURRENT_EVIDENCE_POSTURE.csv",
    "REQUIREMENT_TRACEABILITY_MATRIX.csv",
    "PROVIDER_TEST_SCENARIO_MATRIX.csv",
    "WEBHOOK_AND_EVENT_CUSTODY_REPORT.md",
    "SUBSCRIPTION_LIFECYCLE_ASSURANCE_REPORT.md",
    "RECONCILIATION_AND_CONTROL_TOTAL_REPORT.md",
    "TAX_CALCULATION_BOUNDARY_REPORT.md",
    "SECRET_AND_DATA_HYGIENE_REPORT.md",
    "RESIDUAL_RISK_AND_CONTRADICTORY_EVIDENCE_REGISTER.csv",
    "FOUNDER_CLOSURE_DISPOSITION.md",
}
BUGBOT_FINDINGS = {
    "a7811263-950b-4748-bfef-ff03e0a6ffc9",
    "9b6947a1-d23f-4d1a-9ec5-b26786fad6b1",
    "a5c02c51-35f1-48f3-bed1-f295f0476d31",
    "974dabc2-c3c6-4219-ae6d-e13177f5eeb8",
}
BOUNDARY_TOKENS = {
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_FOUNDER_APPROVAL_REMAINS_VALID",
    "CGP006_MAP_GAP_0005_APPROVED_SOURCE_ZIP_PROTECTEDLY_TRACKED",
    "CGP006_MAP_GAP_0005_ACCESSION_VALIDATOR_HARDENED",
    "CGP006_MAP_GAP_0005_CUSTODY_VALIDATOR_HARDENED",
    "CGP006_MAP_GAP_0005_PROHIBITED_PLACEHOLDER_REJECTION_VERIFIED",
    "CGP006_MAP_GAP_0005_BOUNDARY_TOKEN_SELF_VALIDATION_DEFECT_CORRECTED",
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTED",
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_MERGE_CUSTODY_REFRESH_COMPLETE",
    "CGP006_MAP_GAP_0005_REMAINS_OPEN",
    "PROVIDER_ASSURANCE_MAY_RESUME_ONLY_FROM_PHASE_0_AFTER_REFRESHED_CUSTODY",
    "NO_STRIPE_API_CALL_OCCURRED",
    "NO_STRIPE_SANDBOX_MUTATION_OCCURRED",
    "NO_LIVE_STRIPE_ACCESS_OCCURRED",
    "NO_STRIPE_SECRET_OR_OBJECT_USED",
    "NO_PRODUCT_CODE_CHANGED",
    "NO_SCHEMA_OR_MIGRATION_CHANGED",
    "NO_DEPLOYMENT_AUTHORIZED",
    "NO_STAGING_AUTHORIZED",
    "NO_PILOT_AUTHORIZED",
    "NO_PRODUCTION_USE_AUTHORIZED",
    "NO_PUBLIC_LAUNCH_AUTHORIZED",
    "PR_69_NOT_MODIFIED_OR_MERGED",
    "PR_70_NOT_MODIFIED_OR_MERGED",
}
BOUNDARY_SOURCE_LABELS = {
    "README.md": PACKAGE_PATH / "README.md",
    "CURRENT_STATUS_RECONCILIATION.md": PACKAGE_PATH / "CURRENT_STATUS_RECONCILIATION.md",
    "PLACEHOLDER_REJECTION_VALIDATION_REPORT.md": PACKAGE_PATH / "PLACEHOLDER_REJECTION_VALIDATION_REPORT.md",
    "DIRECTIVE_EXECUTION_RECORD.md": PACKAGE_PATH / "DIRECTIVE_EXECUTION_RECORD.md",
    "receipt": RECEIPT_PATH,
    "PROGRAM_STATUS.md": PROGRAM_STATUS,
}
SECRET_RE = re.compile(r"(sk_live_[A-Za-z0-9_]+|sk_test_[A-Za-z0-9_]+|rk_live_[A-Za-z0-9_]+|rk_test_[A-Za-z0-9_]+|whsec_[A-Za-z0-9_]+|mongodb(?:\+srv)?://|JWT_SECRET\s*=|STRIPE_SECRET_KEY\s*=.+|STRIPE_API_KEY\s*=.+)", re.IGNORECASE)
CONFLICT_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
TEXT_SUFFIXES = {".md", ".py", ".json", ".csv", ".sha256", ""}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[7]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(root: Path, *args: str, check: bool = True) -> str:
    cp = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        raise AssertionError(f"git command failed: {' '.join(args)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
    return cp.stdout.rstrip("\n")


def run_git_bytes(root: Path, *args: str, check: bool = True) -> bytes:
    cp = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        raise AssertionError(f"git command failed: {' '.join(args)}\nSTDERR:\n{cp.stderr.decode('utf-8', errors='replace')}")
    return cp.stdout


def git_tracked_files(root: Path, package: Path) -> set[str]:
    prefix = package.as_posix()
    return {
        path[len(prefix) + 1:]
        for path in run_git(root, "ls-files", prefix).splitlines()
        if path.startswith(prefix + "/")
    }


def git_object_bytes(root: Path, rel: Path) -> bytes:
    rel_text = rel.as_posix()
    run_git(root, "ls-files", "--error-unmatch", rel_text)
    run_git(root, "cat-file", "-e", f"HEAD:{rel_text}")
    return run_git_bytes(root, "show", f"HEAD:{rel_text}")


def load_validator(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def validate_file_hygiene(package: Path, found: set[str]) -> None:
    for rel in sorted(found):
        path = package / rel
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as fh:
                list(csv.reader(fh))
        if path.suffix in TEXT_SUFFIXES:
            data = path.read_text(encoding="utf-8")
            if CONFLICT_RE.search(data):
                raise AssertionError(f"conflict marker found: {rel}")
            if SECRET_RE.search(data):
                raise AssertionError(f"secret-like value found: {rel}")
    receipt = (repo_root() / RECEIPT_PATH).read_text(encoding="utf-8")
    if SECRET_RE.search(receipt) or CONFLICT_RE.search(receipt):
        raise AssertionError("receipt contains secret-like value or conflict marker")


def validate_manifest(package: Path, found: set[str]) -> None:
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != PACKAGE_ID:
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


def validate_correction_merge(root: Path) -> None:
    parents = run_git(root, "show", "-s", "--format=%P", CORRECTION_MERGE).split()
    if parents != [STARTING_PROTECTED_HEAD, CORRECTION_HEAD]:
        raise AssertionError("corrective merge parentage mismatch")
    if run_git(root, "merge-base", "--is-ancestor", CORRECTION_MERGE, "HEAD", check=False) != "":
        # merge-base --is-ancestor writes no output on both success and failure; use return code separately.
        pass
    cp = subprocess.run(["git", "merge-base", "--is-ancestor", CORRECTION_MERGE, "HEAD"], cwd=root)
    if cp.returncode != 0:
        raise AssertionError("corrective merge is not an ancestor of HEAD")


def validate_zip_record(root: Path, package: Path) -> None:
    data = git_object_bytes(root, ZIP_PATH)
    if sha256_bytes(data) != EXPECTED_ZIP_SHA or len(data) != EXPECTED_ZIP_BYTES:
        raise AssertionError("approved ZIP Git object identity mismatch")
    record = json.loads((package / "APPROVED_ZIP_PROTECTED_GIT_OBJECT_RECORD.json").read_text(encoding="utf-8"))
    if record.get("approved_zip_sha256") != EXPECTED_ZIP_SHA or record.get("approved_zip_byte_length") != EXPECTED_ZIP_BYTES:
        raise AssertionError("approved ZIP record identity mismatch")
    if record.get("zip_regenerated_or_repackaged") is not False:
        raise AssertionError("approved ZIP record must prohibit regeneration or repackaging")


def validate_clean_checkout_record(package: Path) -> None:
    record = json.loads((package / "CLEAN_DETACHED_CHECKOUT_RECORD.json").read_text(encoding="utf-8"))
    expected = {
        "clean_checkout_commit": CORRECTION_MERGE,
        "approved_zip_git_sha256": EXPECTED_ZIP_SHA,
        "approved_zip_git_byte_length": EXPECTED_ZIP_BYTES,
        "accession_validator_result": "PASS",
        "custody_validator_result": "PASS",
        "correction_validator_result": "PASS",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise AssertionError(f"clean checkout record mismatch for {key}")
    if record.get("ignored_local_zip_copied") is not False:
        raise AssertionError("clean checkout copied ignored local ZIP")
    if record.get("stripe_activity_occurred") is not False or record.get("provider_assurance_performed") is not False:
        raise AssertionError("clean checkout record indicates unauthorized provider activity")


def validate_boundary_tokens(root: Path, package: Path) -> None:
    rows = read_csv_dicts(package / "BOUNDARY_TOKEN_LOCATION_MATRIX.csv")
    matrix_tokens = {row.get("token", "") for row in rows}
    if matrix_tokens != BOUNDARY_TOKENS:
        raise AssertionError("boundary token matrix does not match required tokens")
    source_texts = load_authoritative_sources(root)
    missing = sorted(token for token in BOUNDARY_TOKENS if not any(token in text for text in source_texts.values()))
    if missing:
        raise AssertionError(f"boundary token missing from authoritative records: {missing}")
    bad = [row for row in rows if row.get("result") != "PASS"]
    if bad:
        raise AssertionError("boundary token matrix contains non-pass rows")
    for row in rows:
        token = row["token"]
        labels = [part.strip() for part in row.get("authoritative_locations", "").split(";") if part.strip()]
        if not labels:
            raise AssertionError(f"boundary token has no claimed authoritative locations: {token}")
        unknown = sorted(label for label in labels if label not in source_texts)
        if unknown:
            raise AssertionError(f"boundary token has unknown source labels: {token}: {unknown}")
        missing_locations = sorted(label for label in labels if token not in source_texts[label])
        if missing_locations:
            raise AssertionError(f"boundary token absent from claimed authoritative locations: {token}: {missing_locations}")


def load_authoritative_sources(root: Path) -> dict[str, str]:
    sources = {}
    for label, rel in BOUNDARY_SOURCE_LABELS.items():
        path = root / rel
        if not path.is_file():
            raise AssertionError(f"boundary source missing: {label}")
        sources[label] = path.read_text(encoding="utf-8")
    return sources


def validate_bugbot_matrix(package: Path) -> None:
    rows = read_csv_dicts(package / "BUGBOT_FINDING_FINAL_DISPOSITION_MATRIX.csv")
    ids = {row.get("finding_id", "") for row in rows}
    if ids != BUGBOT_FINDINGS:
        raise AssertionError("Bugbot finding matrix ID mismatch")
    for row in rows:
        if row.get("corrective_disposition") != "CORRECTED_AND_VERIFIED" or row.get("result") != "PASS":
            raise AssertionError("Bugbot finding matrix contains unresolved row")


def validate_placeholder_absence(root: Path, package: Path) -> None:
    for name in PROHIBITED_PLACEHOLDERS:
        if (root / ACCESSION_PATH / name).exists():
            raise AssertionError(f"prohibited placeholder exists in accession package: {name}")
    report = (package / "PLACEHOLDER_REJECTION_VALIDATION_REPORT.md").read_text(encoding="utf-8")
    for name in PROHIBITED_PLACEHOLDERS:
        if name not in report:
            raise AssertionError(f"placeholder report missing {name}")


def validate_status(root: Path) -> None:
    status = (root / PROGRAM_STATUS).read_text(encoding="utf-8")
    required = {
        "CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_MERGE_CUSTODY_REFRESH_COMPLETE",
        "CGP006_MAP_GAP_0005_REMAINS_OPEN",
        "PROVIDER_ASSURANCE_MAY_RESUME_ONLY_FROM_PHASE_0_AFTER_REFRESHED_CUSTODY",
        "PR_69_NOT_MODIFIED_OR_MERGED",
        "PR_70_NOT_MODIFIED_OR_MERGED",
    }
    missing = sorted(token for token in required if token not in status)
    if missing:
        raise AssertionError(f"PROGRAM_STATUS missing refresh token: {missing}")
    prohibited = [
        "CGP006_MAP_GAP_0005_PROVIDER_ASSURANCE_COMPLETE",
        "PRODUCTION_FINANCIAL_READINESS_ESTABLISHED",
        "PROVIDER_CONNECTED_SANDBOX_LIFECYCLE_ASSURANCE_COMPLETE",
    ]
    for token in prohibited:
        if token in status:
            raise AssertionError(f"PROGRAM_STATUS contains unauthorized closure claim: {token}")


def validate_authorized_paths(root: Path) -> None:
    allowed_prefixes = [PACKAGE_PATH.as_posix() + "/"]
    allowed_files = {PROGRAM_STATUS.as_posix(), RECEIPT_PATH.as_posix()}
    changed = set(run_git(root, "diff", "--name-only", "origin/integrate-emergent-final-zip...HEAD", check=False).splitlines())
    changed.update(run_git(root, "diff", "--name-only", check=False).splitlines())
    changed.update(run_git(root, "diff", "--cached", "--name-only", check=False).splitlines())
    unauthorized = sorted(path for path in changed if path and not (path in allowed_files or any(path.startswith(prefix) for prefix in allowed_prefixes)))
    if unauthorized:
        raise AssertionError(f"unauthorized changed paths: {unauthorized}")


def validate() -> dict[str, object]:
    root = repo_root()
    package = root / PACKAGE_PATH
    if not package.is_dir():
        raise AssertionError(f"refresh package path missing: {PACKAGE_PATH}")
    if not (root / RECEIPT_PATH).is_file():
        raise AssertionError(f"refresh receipt missing: {RECEIPT_PATH}")
    found = git_tracked_files(root, PACKAGE_PATH)
    missing = sorted(REQUIRED_FILES - found)
    if missing:
        raise AssertionError(f"missing tracked refresh package files: {missing}")
    validate_file_hygiene(package, found)
    validate_manifest(package, found)
    validate_correction_merge(root)
    validate_zip_record(root, package)
    validate_clean_checkout_record(package)
    validate_boundary_tokens(root, package)
    validate_bugbot_matrix(package)
    validate_placeholder_absence(root, package)
    validate_status(root)
    validate_authorized_paths(root)
    accession_result = load_validator(root / ACCESSION_VALIDATOR).validate()
    custody_result = load_validator(root / CUSTODY_VALIDATOR).validate()
    correction_result = load_validator(root / CORRECTION_VALIDATOR).validate()
    return {
        "status": "PASS",
        "package_files": len(found),
        "approved_zip_git_sha256": EXPECTED_ZIP_SHA,
        "approved_zip_git_bytes": EXPECTED_ZIP_BYTES,
        "boundary_tokens": len(BOUNDARY_TOKENS),
        "bugbot_findings": len(BUGBOT_FINDINGS),
        "accession_status": accession_result.get("status", "PASS") if isinstance(accession_result, dict) else "PASS",
        "custody_status": custody_result.get("status", "PASS") if isinstance(custody_result, dict) else "PASS",
        "correction_status": correction_result.get("status", "PASS") if isinstance(correction_result, dict) else "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
