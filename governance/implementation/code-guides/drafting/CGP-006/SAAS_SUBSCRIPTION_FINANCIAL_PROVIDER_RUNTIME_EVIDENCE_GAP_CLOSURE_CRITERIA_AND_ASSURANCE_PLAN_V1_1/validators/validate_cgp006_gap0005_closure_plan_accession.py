#!/usr/bin/env python3
"""Validate CGP-006 GAP-0005 closure-plan accession package."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1")
PROGRAM_STATUS = Path("governance/implementation/code-guides/PROGRAM_STATUS.md")
CORRECTION_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_V1")
REFRESH_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2")
REFRESH_RECEIPT = Path("governance/implementation/code-guides/receipts/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2_RECEIPT.md")
DIRECTIVE_ID = "CGP_006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_PROTECTED_ACCESSION_AND_CUSTODY_DIRECTIVE_V1_0_0"
CORRECTION_DIRECTIVE_ID = "CGP_006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_AND_REFRESH_DIRECTIVE_V1_0_0"
FOUNDER_APPROVAL_ID = "ES-FD-CGP006-MAP-GAP-0005-CLOSURE-PLAN-V1.1.0-2026-08-01"
CLASSIFICATION = "FOUNDER_APPROVED_SUBORDINATE_CGP_006_IMPLEMENTATION_GOVERNANCE_ASSURANCE_PLAN"
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
    ".gitattributes",
    "README.md",
    ROOT_MD,
    "APPROVED_SOURCE/" + ZIP_NAME,
    *("APPROVED_SOURCE/" + name for name in APPROVED),
    "FOUNDER_APPROVAL_AND_SOURCE_IDENTITY_RECORD.md",
    "SOURCE_REGISTER.md",
    "AUTHORITY_AND_SCOPE_MATRIX.csv",
    "CURRENT_GAP_STATUS_OVERLAY.md",
    "PLANNED_CLOSURE_ARTIFACT_REGISTER.csv",
    "REPOSITORY_STATE_RECONCILIATION_RECORD.md",
    "ACCESSION_RECORD.md",
    "AUTHORIZED_PATH_REPORT.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "VALIDATION_REPORT.md",
    "validators/validate_cgp006_gap0005_closure_plan_accession.py",
    "tests/test_cgp006_gap0005_closure_plan_accession.py",
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
SECRET_RE = re.compile(r"(sk_live_[A-Za-z0-9_]+|sk_test_[A-Za-z0-9_]+|rk_live_[A-Za-z0-9_]+|rk_test_[A-Za-z0-9_]+|whsec_[A-Za-z0-9_]+|mongodb(?:\+srv)?://|JWT_SECRET\s*=|STRIPE_SECRET_KEY\s*=.+|STRIPE_API_KEY\s*=.+)", re.IGNORECASE)
CONFLICT_MARKER_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
TEXT_SUFFIXES = {".md", ".py", ".json", ".csv", ".sha256", ""}
AUTHORITATIVE_TOKEN_LOCATIONS = {
    DIRECTIVE_ID: {"ACCESSION_RECORD.md", "AUTHORITY_AND_SCOPE_MATRIX.csv", "FOUNDER_APPROVAL_AND_SOURCE_IDENTITY_RECORD.md", "README.md"},
    FOUNDER_APPROVAL_ID: {"ACCESSION_RECORD.md", "AUTHORITY_AND_SCOPE_MATRIX.csv", "FOUNDER_APPROVAL_AND_SOURCE_IDENTITY_RECORD.md", ROOT_MD, "CURRENT_GAP_STATUS_OVERLAY.md"},
    CLASSIFICATION: {"ACCESSION_RECORD.md", "SOURCE_REGISTER.md", "README.md"},
    "CGP006_MAP_GAP_0005_REMAINS_OPEN": {ROOT_MD, "CURRENT_GAP_STATUS_OVERLAY.md"},
    "PROVIDER_CONNECTED_ASSURANCE_WORKSTREAM_NOT_AUTHORIZED_BY_THIS_DIRECTIVE": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "IMPLEMENTATION_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "PROVIDER_ACTIVATION_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "LIVE_PAYMENT_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "NO_CUSTOMER_FUNDS_MOVEMENT_AUTHORIZED": {ROOT_MD, "CURRENT_GAP_STATUS_OVERLAY.md"},
    "PRODUCTION_FINANCIAL_READINESS_NOT_ESTABLISHED": {ROOT_MD, "CURRENT_GAP_STATUS_OVERLAY.md"},
    "DEPLOYMENT_NOT_AUTHORIZED": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "STAGING_NOT_AUTHORIZED": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "PILOT_NOT_AUTHORIZED": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "PRODUCTION_USE_NOT_AUTHORIZED": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "PUBLIC_LAUNCH_NOT_AUTHORIZED": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "PR_69_NOT_MODIFIED_BY_THIS_DIRECTIVE": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "PR_70_NOT_MODIFIED_BY_THIS_DIRECTIVE": {"CURRENT_GAP_STATUS_OVERLAY.md"},
    "UNRELATED_GAPS_FINDINGS_AND_FINANCIAL_PROGRAMS_UNCHANGED": {"CURRENT_GAP_STATUS_OVERLAY.md"},
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


def authoritative_text(package: Path, rel: str) -> str:
    if rel.startswith("validators/") or rel.startswith("tests/"):
        fail(f"non-authoritative token source rejected: {rel}")
    if Path(rel).name in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}:
        fail(f"manifest/checksum cannot satisfy boundary token: {rel}")
    path = package / rel
    return path.read_text(encoding="utf-8")


def validate_boundary_tokens(package: Path) -> dict[str, list[str]]:
    locations: dict[str, list[str]] = {}
    for token, rels in AUTHORITATIVE_TOKEN_LOCATIONS.items():
        found = sorted(rel for rel in rels if token in authoritative_text(package, rel))
        if not found:
            fail(f"required boundary token missing from authoritative governance files: {token}")
        locations[token] = found
    return locations


def validate_git_zip_and_approved_sources(root: Path, package: Path) -> None:
    zip_rel = (PACKAGE_REL / "APPROVED_SOURCE" / ZIP_NAME).as_posix()
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
            repo_rel = (PACKAGE_REL / "APPROVED_SOURCE" / name).as_posix()
            if git_object_bytes(root, repo_rel) != data:
                fail(f"approved source Git object differs from ZIP member: {name}")

        manifest_source = json.loads(zf.read("CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_PACKAGE_MANIFEST.json"))
        if manifest_source.get("founder_approval_id") != FOUNDER_APPROVAL_ID:
            fail("Founder approval ID mismatch in approved manifest")

        checksum_seen = set()
        checksum_lines = zf.read("CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256").decode("utf-8").splitlines()
        for line in checksum_lines:
            if not line.strip():
                continue
            digest, name = line.split(maxsplit=1)
            checksum_seen.add(name)
            if name not in APPROVED:
                fail(f"unexpected file in approved checksum ledger: {name}")
            if digest != APPROVED[name][0]:
                fail(f"approved checksum ledger digest mismatch for {name}")
        expected_checksum_names = set(APPROVED) - {"CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256"}
        if checksum_seen != expected_checksum_names:
            fail("approved checksum ledger inventory mismatch")

    root_md_data = git_object_bytes(root, (PACKAGE_REL / ROOT_MD).as_posix())
    source_md_data = git_object_bytes(root, (PACKAGE_REL / "APPROVED_SOURCE" / SOURCE_MD).as_posix())
    if root_md_data != source_md_data:
        fail("root controlling Markdown is not an exact byte copy")
    if sha256_bytes(root_md_data) != APPROVED[SOURCE_MD][0] or len(root_md_data) != APPROVED[SOURCE_MD][1]:
        fail("root controlling Markdown identity mismatch")


def validate_manifests(package: Path, found: set[str]) -> None:
    package_manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if package_manifest.get("founder_approval_id") != FOUNDER_APPROVAL_ID:
        fail("package manifest Founder approval ID mismatch")
    if package_manifest.get("classification") != CLASSIFICATION:
        fail("package classification mismatch")
    for row in package_manifest.get("files", []):
        rel = row["path"]
        path = package / rel
        if not path.is_file():
            fail(f"manifest file missing: {rel}")
        if sha256(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            fail(f"manifest identity mismatch: {rel}")

    checksum_seen = set()
    for line in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        path = package / rel
        if not path.is_file():
            fail(f"checksum manifest file missing: {rel}")
        if sha256(path) != digest:
            fail(f"checksum manifest digest mismatch: {rel}")
        checksum_seen.add(rel)
    expected_checksum = found - {"CHECKSUM_MANIFEST.sha256"}
    if checksum_seen != expected_checksum:
        fail("checksum manifest inventory mismatch")


def validate_file_hygiene(package: Path, found: set[str]) -> None:
    approved_source_allowed = {"APPROVED_SOURCE/" + ZIP_NAME, *("APPROVED_SOURCE/" + name for name in APPROVED)}
    unexpected_approved_source = sorted(rel for rel in found if rel.startswith("APPROVED_SOURCE/") and rel not in approved_source_allowed)
    if unexpected_approved_source:
        fail(f"unexpected approved-source files: {unexpected_approved_source}")

    extra_placeholders = sorted(PROHIBITED_PLACEHOLDER_EVIDENCE & found)
    if extra_placeholders:
        fail(f"future evidence placeholders must not be created: {extra_placeholders}")

    for rel in sorted(found):
        path = package / rel
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as fh:
                list(csv.reader(fh))
        if path.suffix in TEXT_SUFFIXES:
            data = path.read_text(encoding="utf-8")
            if CONFLICT_MARKER_RE.search(data):
                fail(f"conflict marker found: {rel}")
            if SECRET_RE.search(data):
                fail(f"secret-like value found: {rel}")


def validate_status(root: Path) -> None:
    status = (root / PROGRAM_STATUS).read_text(encoding="utf-8")
    required = ["CGP-006 GAP-0005 Closure Criteria Plan V1.1 Accession Status", FOUNDER_APPROVAL_ID, "CGP006_MAP_GAP_0005_REMAINS_OPEN"]
    for token in required:
        if token not in status:
            fail(f"PROGRAM_STATUS missing bounded status token: {token}")
    normalized = status.replace("CGP006_MAP_GAP_0005_CLOSED`", "")
    if "CGP006_MAP_GAP_0005_CLOSED" in normalized:
        fail("PROGRAM_STATUS appears to close GAP-0005")


def validate_authorized_paths(root: Path) -> None:
    allowed_prefixes = [
        PACKAGE_REL.as_posix() + "/",
        "governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_POST_MERGE_CUSTODY/",
        CORRECTION_PATH.as_posix() + "/",
        REFRESH_PATH.as_posix() + "/",
    ]
    allowed_files = {PROGRAM_STATUS.as_posix(), REFRESH_RECEIPT.as_posix()}
    changed = set(run_git(root, "diff", "--name-only", "origin/integrate-emergent-final-zip...HEAD", check=False).splitlines())
    changed.update(run_git(root, "diff", "--name-only", check=False).splitlines())
    changed.update(run_git(root, "diff", "--cached", "--name-only", check=False).splitlines())
    unauthorized = sorted(path for path in changed if path and not (path in allowed_files or any(path.startswith(prefix) for prefix in allowed_prefixes)))
    if unauthorized:
        fail(f"unauthorized changed paths: {unauthorized}")


def validate() -> dict[str, object]:
    root = repo_root()
    package = root / PACKAGE_REL
    if not package.is_dir():
        fail(f"package path missing: {PACKAGE_REL}")

    found = git_tracked_files(root, PACKAGE_REL)
    missing = sorted(REQUIRED_FILES - found)
    if missing:
        fail(f"required tracked files missing: {missing}")

    validate_git_zip_and_approved_sources(root, package)
    validate_manifests(package, found)
    validate_file_hygiene(package, found)
    boundary_locations = validate_boundary_tokens(package)

    policy_text = "\n".join(
        (package / rel).read_text(encoding="utf-8")
        for rel in found
        if not rel.startswith("validators/")
        and not rel.startswith("tests/")
        and Path(rel).name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
        and (package / rel).suffix in TEXT_SUFFIXES
    )
    if "CGP006_MAP_GAP_0005_CLOSED" in policy_text.replace("Prohibited statement: `CGP006_MAP_GAP_0005_CLOSED`", ""):
        fail("prohibited closure token appears outside explicit prohibited-statement note")

    validate_status(root)
    validate_authorized_paths(root)

    result = {
        "approved_zip_git_sha256": EXPECTED_ZIP_SHA,
        "approved_zip_git_bytes": EXPECTED_ZIP_BYTES,
        "boundary_tokens": len(boundary_locations),
        "package_files": len(found),
        "status": "PASS",
    }
    print("CGP006 GAP-0005 closure plan accession validation PASS")
    return result


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2), file=sys.stderr)
        raise
