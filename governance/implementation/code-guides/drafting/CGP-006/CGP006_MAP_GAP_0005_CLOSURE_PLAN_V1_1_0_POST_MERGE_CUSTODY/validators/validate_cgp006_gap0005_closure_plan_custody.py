#!/usr/bin/env python3
"""Validate CGP-006 GAP-0005 closure-plan post-merge custody package."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ACCESSION_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1")
CUSTODY_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_POST_MERGE_CUSTODY")
CORRECTION_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_V1")
REFRESH_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2")
RECEIPT_PATH = Path("governance/implementation/code-guides/receipts/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_CUSTODY_RECEIPT.md")
REFRESH_RECEIPT = Path("governance/implementation/code-guides/receipts/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2_RECEIPT.md")
PROGRAM_STATUS = Path("governance/implementation/code-guides/PROGRAM_STATUS.md")
DIRECTIVE_ID = "CGP_006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_PROTECTED_ACCESSION_AND_CUSTODY_DIRECTIVE_V1_0_0"
FOUNDER_APPROVAL_ID = "ES-FD-CGP006-MAP-GAP-0005-CLOSURE-PLAN-V1.1.0-2026-08-01"
PACKAGE_ID = "CGP006-MAP-GAP-0005-CLOSURE-PLAN-V1.1.0-POST-MERGE-CUSTODY"
PROTECTED_BRANCH = "integrate-emergent-final-zip"
REVIEWED_REFERENCE_HEAD = "9996e948ede39a968b8facd8afe15c2b1a345204"
PRE_ACCESSION_HEAD = "d0d9528028982c1243f9e2a6b0f21a78f298276c"
ACCESSION_PR_HEAD = "016accf4d6eb35ef2e436bcf26330c5a050dddd8"
ACCESSION_MERGE = "95a4c9b4006f4bd4377f75b3d0fef57d5f424dee"
CUSTODY_BRANCH = "codex/cgp006-gap0005-closure-plan-v1-1-custody"
CUSTODY_PR_PLACEHOLDER = "PR #74 https://github.com/rianray2012-coder/EquineSync-V4/pull/74"
FINAL_CUSTODY_STATE = "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_PROTECTEDLY_ACCESSIONED_AND_POST_MERGE_CUSTODY_COMPLETE_NO_GAP_CLOSURE_EFFECT"
GAP_OPEN = "CGP006_MAP_GAP_0005_REMAINS_OPEN"
ZIP_NAME = "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_2026_08_01.zip"
ROOT_MD = "CGP006_MAP_GAP_0005_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1_0.md"
SOURCE_MD = "CGP006_MAP_GAP_0005_SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1_0_FOUNDER_APPROVED.md"
EXPECTED_ZIP_SHA = "56cec940bef67ca1a6932428398fdde7b3f7e78a9aee9f2b2f8e84b47ea49b95"
EXPECTED_ZIP_BYTES = 117450
APPROVED = {
    SOURCE_MD: ("3dd7774cf35fc160e95209e1c7844028937f62176cbb184cc229d91267fc1bb1", 47636),
    "CGP006_MAP_GAP_0005_SaaS_Subscription_Financial_Provider_Runtime_Evidence_Closure_Criteria_and_Assurance_Plan_V1_1_0_FOUNDER_APPROVED.docx": ("47233460c91e82a59b7bbe5a515d110438f71d690510db3897552e6c7e09f4d3", 61742),
    "FOUNDER_APPROVAL_RECORD_CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_2026_08_01.md": ("da3ae9f93365e6e7587176e273f622f685e605e9785bc74b607174dc0c053f47", 4517),
    "FOUNDER_APPROVAL_RECORD_CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_2026_08_01.docx": ("d9d8fd0f7680b083021d7057258b2f0b99b331f8c205d9eede0e04604922c894", 39846),
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_PACKAGE_MANIFEST.json": ("ef901c7033defeecd9444f58cbca8da822385c3fab3f225ddb21949abe564e32", 1513),
    "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256": ("9f4b551a3cf710c9807f4fa35eefc57713a9ab9987503ecc16e9dc2e9393c9cc", 843),
}
REQUIRED_FILES = {
    "AUTHORIZED_PATH_REPORT.md",
    "CHECKSUM_MANIFEST.sha256",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "PACKAGE_MANIFEST.json",
    "POST_MERGE_PROTECTED_HEAD_RECORD.json",
    "PROTECTED_MERGE_RECEIPT.json",
    "README.md",
    "SOURCE_IDENTITY_REGISTER.csv",
    "VALIDATION_REPORT.md",
    "tests/test_cgp006_gap0005_closure_plan_custody.py",
    "validators/validate_cgp006_gap0005_closure_plan_custody.py",
}
PROHIBITED_PLACEHOLDER_EVIDENCE = {
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
SECRET_RE = re.compile(
    r"(sk_live_[A-Za-z0-9_]+|sk_test_[A-Za-z0-9_]+|rk_live_[A-Za-z0-9_]+|rk_test_[A-Za-z0-9_]+|whsec_[A-Za-z0-9_]+|mongodb(?:\+srv)?://|JWT_SECRET\s*=|STRIPE_SECRET_KEY\s*=.+|STRIPE_API_KEY\s*=.+)",
    re.IGNORECASE,
)
CONFLICT_MARKER_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
TEXT_SUFFIXES = {".md", ".py", ".json", ".csv", ".sha256", ""}
AUTHORITATIVE_TOKEN_LOCATIONS = {
    DIRECTIVE_ID: {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "PROTECTED_MERGE_RECEIPT.json"},
    FOUNDER_APPROVAL_ID: {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "PROTECTED_MERGE_RECEIPT.json"},
    FINAL_CUSTODY_STATE: {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    GAP_OPEN: {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PROVIDER_CONNECTED_ASSURANCE_WORKSTREAM_NOT_AUTHORIZED_BY_THIS_DIRECTIVE": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "IMPLEMENTATION_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PROVIDER_ACTIVATION_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "LIVE_PAYMENT_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "NO_CUSTOMER_FUNDS_MOVEMENT_AUTHORIZED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PRODUCTION_FINANCIAL_READINESS_NOT_ESTABLISHED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "DEPLOYMENT_NOT_AUTHORIZED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "STAGING_NOT_AUTHORIZED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PILOT_NOT_AUTHORIZED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PRODUCTION_USE_NOT_AUTHORIZED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PUBLIC_LAUNCH_NOT_AUTHORIZED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "PR_69_NOT_MODIFIED_BY_THIS_DIRECTIVE": {RECEIPT_PATH, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "AUTHORIZED_PATH_REPORT.md"},
    "PR_70_NOT_MODIFIED_BY_THIS_DIRECTIVE": {RECEIPT_PATH, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "AUTHORIZED_PATH_REPORT.md"},
    "NO_ADDITIONAL_STRIPE_MUTATION_DURING_CUSTODY": {RECEIPT_PATH, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "NO_LIVE_STRIPE_MUTATION_RECORDED": {RECEIPT_PATH, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "NO_LIVE_STRIPE_OBJECT_OR_SECRET_USED": {RECEIPT_PATH, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "NO_SECRET_DISCLOSURE": {RECEIPT_PATH, CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md", CUSTODY_PATH / "VALIDATION_REPORT.md"},
    "UNRELATED_GAPS_FINDINGS_AND_FINANCIAL_PROGRAMS_UNCHANGED": {RECEIPT_PATH, PROGRAM_STATUS, CUSTODY_PATH / "README.md", CUSTODY_PATH / "DIRECTIVE_EXECUTION_RECORD.md"},
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[7]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def fail(msg: str) -> None:
    raise AssertionError(msg)


def run_git(root: Path, *args: str, check: bool = True) -> str:
    cp = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        fail(f"git command failed: {' '.join(args)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
    return cp.stdout.rstrip("\n")


def run_git_bytes(root: Path, *args: str, check: bool = True) -> bytes:
    cp = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        fail(f"git command failed: {' '.join(args)}\nSTDERR:\n{cp.stderr.decode('utf-8', errors='replace')}")
    return cp.stdout


def git_object_bytes(root: Path, rel: str) -> bytes:
    run_git(root, "ls-files", "--error-unmatch", rel)
    run_git(root, "cat-file", "-e", f"HEAD:{rel}")
    return run_git_bytes(root, "show", f"HEAD:{rel}")


def git_tracked_files(root: Path, package: Path) -> set[str]:
    prefix = package.as_posix()
    return {
        path[len(prefix) + 1:]
        for path in run_git(root, "ls-files", prefix).splitlines()
        if path.startswith(prefix + "/")
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def run_accession_validation(root: Path) -> dict[str, object] | None:
    validator_path = root / ACCESSION_PATH / "validators" / "validate_cgp006_gap0005_closure_plan_accession.py"
    spec = importlib.util.spec_from_file_location("validate_cgp006_gap0005_closure_plan_accession_dependency", validator_path)
    if spec is None or spec.loader is None:
        fail("unable to load corrected accession validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate()


def validate_boundary_tokens(root: Path) -> dict[str, list[str]]:
    locations: dict[str, list[str]] = {}
    for token, rels in AUTHORITATIVE_TOKEN_LOCATIONS.items():
        found: list[str] = []
        for rel in sorted(rels, key=lambda value: value.as_posix()):
            if "validators" in rel.parts or "tests" in rel.parts or rel.name in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}:
                fail(f"non-authoritative token source configured: {rel}")
            path = root / rel
            if not path.is_file():
                continue
            if token in path.read_text(encoding="utf-8"):
                found.append(rel.as_posix())
        if not found:
            fail(f"required custody boundary token missing from authoritative governance files: {token}")
        locations[token] = found
    return locations


def validate_git_zip_object(root: Path) -> None:
    zip_rel = (ACCESSION_PATH / "APPROVED_SOURCE" / ZIP_NAME).as_posix()
    zip_data = git_object_bytes(root, zip_rel)
    if sha256_bytes(zip_data) != EXPECTED_ZIP_SHA or len(zip_data) != EXPECTED_ZIP_BYTES:
        fail("approved source ZIP Git object identity mismatch")
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        names = sorted(name for name in zf.namelist() if not name.endswith("/"))
        if names != sorted(APPROVED):
            fail(f"ZIP inventory mismatch: {names}")
        bad = zf.testzip()
        if bad is not None:
            fail(f"ZIP integrity failure at {bad}")
        for name, (expected_sha, expected_bytes) in APPROVED.items():
            data = zf.read(name)
            if sha256_bytes(data) != expected_sha or len(data) != expected_bytes:
                fail(f"approved ZIP member identity mismatch: {name}")
            repo_rel = (ACCESSION_PATH / "APPROVED_SOURCE" / name).as_posix()
            if git_object_bytes(root, repo_rel) != data:
                fail(f"approved source Git object differs from ZIP member: {name}")


def validate_accession_placeholder_prohibitions(root: Path) -> None:
    accession_files = git_tracked_files(root, ACCESSION_PATH)
    offending = sorted(
        rel for rel in accession_files
        if rel in PROHIBITED_PLACEHOLDER_EVIDENCE or Path(rel).name in PROHIBITED_PLACEHOLDER_EVIDENCE
    )
    if offending:
        fail(f"prohibited future-evidence placeholders in accession tree: {offending}")


def assert_checksum_manifest(package: Path, found: set[str]) -> None:
    seen: set[str] = set()
    for raw in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        expected, rel = raw.split(maxsplit=1)
        path = package / rel
        if not path.is_file():
            fail(f"checksum manifest file missing: {rel}")
        if sha256(path) != expected:
            fail(f"checksum manifest digest mismatch: {rel}")
        seen.add(rel)
    expected = found - {"CHECKSUM_MANIFEST.sha256"}
    if seen != expected:
        fail("checksum manifest inventory mismatch")


def validate_custody_files(root: Path, package: Path, found: set[str]) -> None:
    missing = sorted(REQUIRED_FILES - found)
    if missing:
        fail(f"missing custody artifacts: {missing}")
    for rel in sorted(found):
        path = package / rel
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        if path.suffix == ".csv":
            read_csv(path)
        if path.suffix in TEXT_SUFFIXES:
            data = path.read_text(encoding="utf-8")
            if CONFLICT_MARKER_RE.search(data):
                fail(f"conflict marker found: {rel}")
            if SECRET_RE.search(data):
                fail(f"secret-like value found: {rel}")

    for rel in [RECEIPT_PATH, PROGRAM_STATUS]:
        data = (root / rel).read_text(encoding="utf-8")
        if CONFLICT_MARKER_RE.search(data):
            fail(f"conflict marker found: {rel}")
        if SECRET_RE.search(data):
            fail(f"secret-like value found: {rel}")


def validate_custody_manifest(package: Path, found: set[str]) -> None:
    assert_checksum_manifest(package, found)
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != PACKAGE_ID:
        fail("custody package ID mismatch")
    if manifest.get("protected_branch") != PROTECTED_BRANCH:
        fail("custody package protected branch mismatch")
    for row in manifest.get("files", []):
        path = package / row["path"]
        if not path.is_file():
            fail(f"manifest file missing: {row['path']}")
        if sha256(path) != row["sha256"] or path.stat().st_size != row["byte_length"]:
            fail(f"manifest identity mismatch: {row['path']}")


def validate_merge_identity(root: Path, package: Path) -> None:
    receipt = json.loads((package / "PROTECTED_MERGE_RECEIPT.json").read_text(encoding="utf-8"))
    head_record = json.loads((package / "POST_MERGE_PROTECTED_HEAD_RECORD.json").read_text(encoding="utf-8"))
    expected_pairs = {
        "reviewed_reference_head": REVIEWED_REFERENCE_HEAD,
        "pre_accession_protected_head": PRE_ACCESSION_HEAD,
        "accession_pr_head": ACCESSION_PR_HEAD,
        "accession_merge_commit_sha": ACCESSION_MERGE,
        "post_accession_protected_head": ACCESSION_MERGE,
        "custody_branch": CUSTODY_BRANCH,
    }
    for key, expected in expected_pairs.items():
        if receipt.get(key) != expected:
            fail(f"protected merge receipt mismatch: {key}")
    if head_record["accession_merge_parents"] != [PRE_ACCESSION_HEAD, ACCESSION_PR_HEAD]:
        fail("head record merge parents mismatch")

    parents = run_git(root, "show", "--no-patch", "--format=%P", ACCESSION_MERGE).split()
    if parents != [PRE_ACCESSION_HEAD, ACCESSION_PR_HEAD]:
        fail(f"accession merge parents mismatch: {parents}")
    run_git(root, "merge-base", "--is-ancestor", ACCESSION_PR_HEAD, ACCESSION_MERGE)
    run_git(root, "merge-base", "--is-ancestor", ACCESSION_MERGE, "HEAD")


def validate_source_identity_register(root: Path, package: Path) -> int:
    source_rows = read_csv(package / "SOURCE_IDENTITY_REGISTER.csv")
    if len(source_rows) != 8:
        fail("source identity register row count mismatch")
    for row in source_rows:
        path = root / row["path"]
        if not path.is_file():
            fail(f"source identity path missing: {row['path']}")
        data = git_object_bytes(root, row["path"])
        if sha256_bytes(data) != row["sha256"] or len(data) != int(row["byte_length"]):
            fail(f"source identity Git object mismatch: {row['record_id']}")
        if row["verification_result"] != "PASS":
            fail(f"source identity result not PASS: {row['record_id']}")
    return len(source_rows)


def validate_status_and_claims(root: Path) -> None:
    text = "\n".join((root / rel).read_text(encoding="utf-8") for rel in [RECEIPT_PATH, PROGRAM_STATUS])
    text += "\n" + "\n".join(
        path.read_text(encoding="utf-8")
        for path in (root / CUSTODY_PATH).rglob("*")
        if path.is_file()
        and "validators" not in path.parts
        and "tests" not in path.parts
        and path.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
        and path.suffix in TEXT_SUFFIXES
    )
    if GAP_OPEN not in text:
        fail("GAP-0005 open status missing")
    if "CGP006_MAP_GAP_0005_CLOSED" in text.replace("Prohibited statement: `CGP006_MAP_GAP_0005_CLOSED`", ""):
        fail("prohibited closure token appears outside explicit prohibited-statement note")
    prohibited_claims = [
        "CGP006_MAP_GAP_0005_PROVIDER_ASSURANCE_COMPLETE",
        "PRODUCTION_FINANCIAL_READINESS_ESTABLISHED",
        "PROVIDER_CONNECTED_SANDBOX_LIFECYCLE_ASSURANCE_COMPLETE",
    ]
    for token in prohibited_claims:
        if token in text:
            fail(f"unauthorized provider or production readiness claim found: {token}")


def validate_authorized_paths(root: Path) -> None:
    allowed_prefixes = [
        ACCESSION_PATH.as_posix() + "/",
        CUSTODY_PATH.as_posix() + "/",
        CORRECTION_PATH.as_posix() + "/",
        REFRESH_PATH.as_posix() + "/",
    ]
    allowed_files = {PROGRAM_STATUS.as_posix(), RECEIPT_PATH.as_posix(), REFRESH_RECEIPT.as_posix()}
    changed = set(run_git(root, "diff", "--name-only", "origin/integrate-emergent-final-zip...HEAD", check=False).splitlines())
    changed.update(run_git(root, "diff", "--name-only", check=False).splitlines())
    changed.update(run_git(root, "diff", "--cached", "--name-only", check=False).splitlines())
    unauthorized = sorted(path for path in changed if path and not (path in allowed_files or any(path.startswith(prefix) for prefix in allowed_prefixes)))
    if unauthorized:
        fail(f"unauthorized changed paths: {unauthorized}")


def validate() -> dict[str, object]:
    root = repo_root()
    package = root / CUSTODY_PATH
    if not package.is_dir():
        fail(f"custody package path missing: {CUSTODY_PATH}")
    if not (root / RECEIPT_PATH).is_file():
        fail(f"custody receipt missing: {RECEIPT_PATH}")

    accession_result = run_accession_validation(root)
    validate_git_zip_object(root)
    validate_accession_placeholder_prohibitions(root)

    found = git_tracked_files(root, CUSTODY_PATH)
    validate_custody_files(root, package, found)
    validate_custody_manifest(package, found)
    validate_merge_identity(root, package)
    source_identity_rows = validate_source_identity_register(root, package)
    boundary_locations = validate_boundary_tokens(root)
    validate_status_and_claims(root)
    validate_authorized_paths(root)

    run_git(root, "diff", "--check", "origin/integrate-emergent-final-zip...HEAD")
    run_git(root, "diff", "--check")
    run_git(root, "diff", "--cached", "--check")

    return {
        "accession_dependency_status": (accession_result or {}).get("status", "PASS"),
        "accession_merge_commit": ACCESSION_MERGE,
        "approved_zip_git_sha256": EXPECTED_ZIP_SHA,
        "approved_zip_git_bytes": EXPECTED_ZIP_BYTES,
        "boundary_tokens": len(boundary_locations),
        "custody_branch": CUSTODY_BRANCH,
        "custody_files": len(found),
        "custody_pr": CUSTODY_PR_PLACEHOLDER,
        "gap_status": GAP_OPEN,
        "required_artifacts": len(REQUIRED_FILES),
        "source_identity_rows": source_identity_rows,
        "status": "PASS",
    }


def main() -> int:
    try:
        result = validate()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
