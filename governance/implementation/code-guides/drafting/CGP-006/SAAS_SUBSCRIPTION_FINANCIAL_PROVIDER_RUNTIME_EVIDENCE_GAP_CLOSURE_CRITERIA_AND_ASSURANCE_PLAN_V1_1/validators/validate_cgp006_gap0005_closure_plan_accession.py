#!/usr/bin/env python3
"""Validate CGP-006 GAP-0005 closure-plan accession package."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1")
DIRECTIVE_ID = "CGP_006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_PROTECTED_ACCESSION_AND_CUSTODY_DIRECTIVE_V1_0_0"
FOUNDER_APPROVAL_ID = "ES-FD-CGP006-MAP-GAP-0005-CLOSURE-PLAN-V1.1.0-2026-08-01"
CLASSIFICATION = "FOUNDER_APPROVED_SUBORDINATE_CGP_006_IMPLEMENTATION_GOVERNANCE_ASSURANCE_PLAN"
START_HEAD = "d0d9528028982c1243f9e2a6b0f21a78f298276c"
REVIEWED_REF = "9996e948ede39a968b8facd8afe15c2b1a345204"
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
BOUNDARY_TOKENS = [
    DIRECTIVE_ID,
    FOUNDER_APPROVAL_ID,
    CLASSIFICATION,
    "CGP006_MAP_GAP_0005_REMAINS_OPEN",
    "PROVIDER_CONNECTED_ASSURANCE_WORKSTREAM_NOT_AUTHORIZED_BY_THIS_DIRECTIVE",
    "IMPLEMENTATION_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE",
    "PROVIDER_ACTIVATION_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE",
    "LIVE_PAYMENT_AUTHORITY_NOT_CREATED_BY_THIS_DIRECTIVE",
    "NO_CUSTOMER_FUNDS_MOVEMENT_AUTHORIZED",
    "PRODUCTION_FINANCIAL_READINESS_NOT_ESTABLISHED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "STAGING_NOT_AUTHORIZED",
    "PILOT_NOT_AUTHORIZED",
    "PRODUCTION_USE_NOT_AUTHORIZED",
    "PUBLIC_LAUNCH_NOT_AUTHORIZED",
    "PR_69_NOT_MODIFIED_BY_THIS_DIRECTIVE",
    "PR_70_NOT_MODIFIED_BY_THIS_DIRECTIVE",
    "UNRELATED_GAPS_FINDINGS_AND_FINANCIAL_PROGRAMS_UNCHANGED",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[7]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def size(path: Path) -> int:
    return path.stat().st_size


def fail(msg: str) -> None:
    raise AssertionError(msg)


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def validate() -> None:
    root = repo_root()
    package = root / PACKAGE_REL
    if not package.is_dir():
        fail(f"package path missing: {PACKAGE_REL}")

    found = {
        str(path.relative_to(package))
        for path in package.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }
    missing = sorted(REQUIRED_FILES - found)
    extra_placeholders = sorted(PROHIBITED_PLACEHOLDER_EVIDENCE & found)
    if missing:
        fail(f"required files missing: {missing}")
    if extra_placeholders:
        fail(f"future evidence placeholders must not be created: {extra_placeholders}")

    zip_path = package / "APPROVED_SOURCE" / ZIP_NAME
    if sha256(zip_path) != EXPECTED_ZIP_SHA or size(zip_path) != EXPECTED_ZIP_BYTES:
        fail("source ZIP identity mismatch")
    with zipfile.ZipFile(zip_path) as zf:
        names = sorted(name for name in zf.namelist() if not name.endswith("/"))
        if names != sorted(APPROVED):
            fail(f"ZIP inventory mismatch: {names}")
        bad = zf.testzip()
        if bad is not None:
            fail(f"ZIP integrity failure at {bad}")

    for name, (expected_sha, expected_bytes) in APPROVED.items():
        path = package / "APPROVED_SOURCE" / name
        if sha256(path) != expected_sha or size(path) != expected_bytes:
            fail(f"approved source identity mismatch: {name}")

    root_md = package / ROOT_MD
    source_md = package / "APPROVED_SOURCE" / SOURCE_MD
    if root_md.read_bytes() != source_md.read_bytes():
        fail("root controlling Markdown is not an exact byte copy")
    if sha256(root_md) != APPROVED[SOURCE_MD][0] or size(root_md) != APPROVED[SOURCE_MD][1]:
        fail("root controlling Markdown identity mismatch")

    manifest_source = json.loads((package / "APPROVED_SOURCE" / "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest_source.get("founder_approval_id") != FOUNDER_APPROVAL_ID:
        fail("Founder approval ID mismatch in approved manifest")

    checksum_lines = (package / "APPROVED_SOURCE" / "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines()
    checksum_names = []
    for line in checksum_lines:
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        checksum_names.append(name)
        if name not in APPROVED:
            fail(f"unexpected file in approved checksum ledger: {name}")
        if digest != APPROVED[name][0]:
            fail(f"approved checksum ledger digest mismatch for {name}")
    expected_checksum_names = sorted(
        name for name in APPROVED
        if name != "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256"
    )
    if sorted(checksum_names) != expected_checksum_names:
        fail("approved checksum ledger inventory mismatch")

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
        if sha256(path) != row["sha256"] or size(path) != row["bytes"]:
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

    for rel in sorted(found):
        path = package / rel
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as fh:
                list(csv.reader(fh))
        if path.suffix in {".md", ".py", ".json", ".csv", ".sha256", ""}:
            data = path.read_text(encoding="utf-8")
            if CONFLICT_MARKER_RE.search(data):
                fail(f"conflict marker found: {rel}")
            if SECRET_RE.search(data):
                fail(f"secret-like value found: {rel}")

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in package.rglob("*")
        if path.is_file() and path.suffix in {".md", ".csv", ".json", ".py", ".sha256", ""}
    )
    policy_combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in package.rglob("*")
        if path.is_file()
        and "validators" not in path.parts
        and "tests" not in path.parts
        and path.suffix in {".md", ".csv", ".json", ".sha256", ""}
    )
    for token in BOUNDARY_TOKENS:
        if token not in combined:
            fail(f"required boundary token missing: {token}")
    if "CGP006_MAP_GAP_0005_CLOSED" in policy_combined.replace("Prohibited statement: `CGP006_MAP_GAP_0005_CLOSED`", ""):
        fail("prohibited closure token appears outside explicit prohibited-statement note")

    status = (root / "governance/implementation/code-guides/PROGRAM_STATUS.md").read_text(encoding="utf-8")
    for token in ["CGP-006 GAP-0005 Closure Criteria Plan V1.1 Accession Status", FOUNDER_APPROVAL_ID, "CGP006_MAP_GAP_0005_REMAINS_OPEN"]:
        if token not in status:
            fail(f"PROGRAM_STATUS missing bounded status token: {token}")

    diff_names = run_git(root, "diff", "--name-only", "origin/integrate-emergent-final-zip...HEAD").splitlines()
    allowed_prefix = PACKAGE_REL.as_posix() + "/"
    allowed_status = "governance/implementation/code-guides/PROGRAM_STATUS.md"
    unauthorized = [name for name in diff_names if not (name.startswith(allowed_prefix) or name == allowed_status)]
    if unauthorized:
        fail(f"unauthorized changed paths: {unauthorized}")

    print("CGP006 GAP-0005 closure plan accession validation PASS")


if __name__ == "__main__":
    validate()
