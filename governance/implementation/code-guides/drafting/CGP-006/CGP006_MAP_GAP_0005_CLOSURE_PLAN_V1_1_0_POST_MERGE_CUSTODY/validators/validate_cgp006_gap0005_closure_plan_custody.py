#!/usr/bin/env python3
"""Validate CGP-006 GAP-0005 closure-plan post-merge custody package."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ACCESSION_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/SAAS_SUBSCRIPTION_FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_GAP_CLOSURE_CRITERIA_AND_ASSURANCE_PLAN_V1_1")
CUSTODY_PATH = Path("governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_POST_MERGE_CUSTODY")
RECEIPT_PATH = Path("governance/implementation/code-guides/receipts/CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_CUSTODY_RECEIPT.md")
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
BOUNDARY_TOKENS = [
    DIRECTIVE_ID,
    FOUNDER_APPROVAL_ID,
    FINAL_CUSTODY_STATE,
    GAP_OPEN,
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
    "NO_ADDITIONAL_STRIPE_MUTATION_DURING_CUSTODY",
    "NO_LIVE_STRIPE_MUTATION_RECORDED",
    "NO_LIVE_STRIPE_OBJECT_OR_SECRET_USED",
    "NO_SECRET_DISCLOSURE",
    "UNRELATED_GAPS_FINDINGS_AND_FINANCIAL_PROGRAMS_UNCHANGED",
]
SECRET_RE = re.compile(
    r"(sk_live_[A-Za-z0-9_]+|sk_test_[A-Za-z0-9_]+|rk_live_[A-Za-z0-9_]+|rk_test_[A-Za-z0-9_]+|whsec_[A-Za-z0-9_]+|mongodb(?:\+srv)?://|JWT_SECRET\s*=|STRIPE_SECRET_KEY\s*=.+|STRIPE_API_KEY\s*=.+)",
    re.IGNORECASE,
)
CONFLICT_MARKER_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[7]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_git(root: Path, *args: str, check: bool = True) -> str:
    cp = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        raise AssertionError(
            f"git command failed: {' '.join(args)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}"
        )
    return cp.stdout.rstrip("\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def custody_files(package: Path) -> set[str]:
    return {
        str(path.relative_to(package))
        for path in package.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }


def assert_checksum_manifest(package: Path, found: set[str]) -> None:
    seen: set[str] = set()
    for raw in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        expected, rel = raw.split(maxsplit=1)
        path = package / rel
        if not path.is_file():
            raise AssertionError(f"checksum manifest file missing: {rel}")
        if sha256(path) != expected:
            raise AssertionError(f"checksum manifest digest mismatch: {rel}")
        seen.add(rel)
    expected = found - {"CHECKSUM_MANIFEST.sha256"}
    if seen != expected:
        raise AssertionError("checksum manifest inventory mismatch")


def assert_accession_source(root: Path) -> None:
    accession = root / ACCESSION_PATH
    zip_path = accession / "APPROVED_SOURCE" / ZIP_NAME
    if sha256(zip_path) != EXPECTED_ZIP_SHA or zip_path.stat().st_size != EXPECTED_ZIP_BYTES:
        raise AssertionError("source ZIP identity mismatch")
    with zipfile.ZipFile(zip_path) as zf:
        names = sorted(name for name in zf.namelist() if not name.endswith("/"))
        if names != sorted(APPROVED):
            raise AssertionError(f"ZIP inventory mismatch: {names}")
        bad = zf.testzip()
        if bad is not None:
            raise AssertionError(f"ZIP integrity failure at {bad}")

    for name, (expected_sha, expected_bytes) in APPROVED.items():
        path = accession / "APPROVED_SOURCE" / name
        if sha256(path) != expected_sha or path.stat().st_size != expected_bytes:
            raise AssertionError(f"approved source identity mismatch: {name}")

    root_md = accession / ROOT_MD
    source_md = accession / "APPROVED_SOURCE" / SOURCE_MD
    if root_md.read_bytes() != source_md.read_bytes():
        raise AssertionError("root controlling Markdown is not an exact byte copy")
    if sha256(root_md) != APPROVED[SOURCE_MD][0] or root_md.stat().st_size != APPROVED[SOURCE_MD][1]:
        raise AssertionError("root controlling Markdown identity mismatch")

    checksum_seen = set()
    for raw in (accession / "APPROVED_SOURCE" / "CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, name = raw.split(maxsplit=1)
        if name not in APPROVED:
            raise AssertionError(f"unexpected approved checksum path: {name}")
        if digest != APPROVED[name][0]:
            raise AssertionError(f"approved checksum digest mismatch: {name}")
        checksum_seen.add(name)
    expected_checksum = set(APPROVED) - {"CGP006_MAP_GAP_0005_CLOSURE_PLAN_V1_1_0_FOUNDER_APPROVED_CHECKSUMS.sha256"}
    if checksum_seen != expected_checksum:
        raise AssertionError("approved checksum ledger inventory mismatch")

    accession_manifest = json.loads((accession / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if accession_manifest.get("accession_pr") != "PR #73 https://github.com/rianray2012-coder/EquineSync-V4/pull/73":
        raise AssertionError("accession package PR record mismatch")
    for row in accession_manifest.get("files", []):
        path = accession / row["path"]
        if not path.is_file():
            raise AssertionError(f"accession manifest file missing: {row['path']}")
        if sha256(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise AssertionError(f"accession manifest identity mismatch: {row['path']}")


def assert_authorized_paths(root: Path) -> None:
    allowed_prefix = CUSTODY_PATH.as_posix() + "/"
    allowed = {PROGRAM_STATUS.as_posix(), RECEIPT_PATH.as_posix()}

    changed = set(run_git(root, "diff", "--name-only", ACCESSION_MERGE, "HEAD", check=False).splitlines())
    changed.update(run_git(root, "diff", "--name-only", check=False).splitlines())
    changed.update(run_git(root, "diff", "--cached", "--name-only", check=False).splitlines())
    unauthorized = sorted(path for path in changed if path and not (path.startswith(allowed_prefix) or path in allowed))
    if unauthorized:
        raise AssertionError(f"unauthorized changed paths: {unauthorized}")

    status_lines = run_git(root, "status", "--short", "--untracked-files=all", check=False).splitlines()
    bad_status = []
    for line in status_lines:
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path and not (path.startswith(allowed_prefix) or path in allowed):
            bad_status.append(line)
    if bad_status:
        raise AssertionError(f"unauthorized worktree paths: {bad_status}")


def validate() -> dict[str, object]:
    root = repo_root()
    package = root / CUSTODY_PATH
    if not package.is_dir():
        raise AssertionError(f"custody package path missing: {CUSTODY_PATH}")
    if not (root / RECEIPT_PATH).is_file():
        raise AssertionError(f"custody receipt missing: {RECEIPT_PATH}")

    found = custody_files(package)
    missing = sorted(REQUIRED_FILES - found)
    if missing:
        raise AssertionError(f"missing custody artifacts: {missing}")

    for path in package.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        if path.suffix == ".csv":
            read_csv(path)
        if path.suffix in {".md", ".py", ".json", ".csv", ".sha256", ""}:
            data = path.read_text(encoding="utf-8")
            if CONFLICT_MARKER_RE.search(data):
                raise AssertionError(f"conflict marker found: {path.relative_to(package)}")
            if SECRET_RE.search(data):
                raise AssertionError(f"secret-like value found: {path.relative_to(package)}")

    for path in [root / RECEIPT_PATH, root / PROGRAM_STATUS]:
        data = path.read_text(encoding="utf-8")
        if CONFLICT_MARKER_RE.search(data):
            raise AssertionError(f"conflict marker found: {path.relative_to(root)}")
        if SECRET_RE.search(data):
            raise AssertionError(f"secret-like value found: {path.relative_to(root)}")

    assert_checksum_manifest(package, found)
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != PACKAGE_ID:
        raise AssertionError("custody package ID mismatch")
    if manifest.get("protected_branch") != PROTECTED_BRANCH:
        raise AssertionError("custody package protected branch mismatch")
    for row in manifest.get("files", []):
        path = package / row["path"]
        if not path.is_file():
            raise AssertionError(f"manifest file missing: {row['path']}")
        if sha256(path) != row["sha256"] or path.stat().st_size != row["byte_length"]:
            raise AssertionError(f"manifest identity mismatch: {row['path']}")

    receipt = json.loads((package / "PROTECTED_MERGE_RECEIPT.json").read_text(encoding="utf-8"))
    head_record = json.loads((package / "POST_MERGE_PROTECTED_HEAD_RECORD.json").read_text(encoding="utf-8"))
    if receipt["reviewed_reference_head"] != REVIEWED_REFERENCE_HEAD:
        raise AssertionError("reviewed reference head mismatch")
    if receipt["pre_accession_protected_head"] != PRE_ACCESSION_HEAD:
        raise AssertionError("pre-accession protected head mismatch")
    if receipt["accession_pr_head"] != ACCESSION_PR_HEAD:
        raise AssertionError("accession PR head mismatch")
    if receipt["accession_merge_commit_sha"] != ACCESSION_MERGE:
        raise AssertionError("accession merge commit mismatch")
    if receipt["post_accession_protected_head"] != ACCESSION_MERGE:
        raise AssertionError("post-accession protected head mismatch")
    if receipt["custody_branch"] != CUSTODY_BRANCH:
        raise AssertionError("custody branch mismatch")
    if head_record["accession_merge_parents"] != [PRE_ACCESSION_HEAD, ACCESSION_PR_HEAD]:
        raise AssertionError("head record merge parents mismatch")

    parents = run_git(root, "show", "--no-patch", "--format=%P", ACCESSION_MERGE).split()
    if parents != [PRE_ACCESSION_HEAD, ACCESSION_PR_HEAD]:
        raise AssertionError(f"accession merge parents mismatch: {parents}")
    run_git(root, "merge-base", "--is-ancestor", ACCESSION_PR_HEAD, ACCESSION_MERGE)
    run_git(root, "merge-base", "--is-ancestor", ACCESSION_MERGE, "HEAD")

    assert_accession_source(root)

    source_rows = read_csv(package / "SOURCE_IDENTITY_REGISTER.csv")
    if len(source_rows) != 8:
        raise AssertionError("source identity register row count mismatch")
    for row in source_rows:
        path = root / row["path"]
        if not path.is_file():
            raise AssertionError(f"source identity path missing: {row['path']}")
        if sha256(path) != row["sha256"] or path.stat().st_size != int(row["byte_length"]):
            raise AssertionError(f"source identity mismatch: {row['record_id']}")
        if row["verification_result"] != "PASS":
            raise AssertionError(f"source identity result not PASS: {row['record_id']}")

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [root / RECEIPT_PATH, root / PROGRAM_STATUS]
    )
    combined += "\n" + "\n".join(
        path.read_text(encoding="utf-8")
        for path in package.rglob("*")
        if path.is_file() and path.suffix in {".md", ".csv", ".json", ".py", ".sha256", ""}
    )
    for token in BOUNDARY_TOKENS:
        if token not in combined:
            raise AssertionError(f"required boundary token missing: {token}")

    policy_combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [root / RECEIPT_PATH, root / PROGRAM_STATUS]
    )
    policy_combined += "\n" + "\n".join(
        path.read_text(encoding="utf-8")
        for path in package.rglob("*")
        if path.is_file()
        and "validators" not in path.parts
        and "tests" not in path.parts
        and path.suffix in {".md", ".csv", ".json", ".sha256", ""}
    )
    if "CGP006_MAP_GAP_0005_CLOSED" in policy_combined.replace("Prohibited statement: `CGP006_MAP_GAP_0005_CLOSED`", ""):
        raise AssertionError("prohibited closure token appears outside explicit prohibited-statement note")

    assert_authorized_paths(root)
    run_git(root, "diff", "--check", ACCESSION_MERGE, "HEAD")
    run_git(root, "diff", "--check")
    run_git(root, "diff", "--cached", "--check")

    return {
        "accession_merge_commit": ACCESSION_MERGE,
        "custody_branch": CUSTODY_BRANCH,
        "custody_files": len(found),
        "custody_pr": manifest.get("custody_pr", CUSTODY_PR_PLACEHOLDER),
        "gap_status": GAP_OPEN,
        "required_artifacts": len(REQUIRED_FILES),
        "source_identity_rows": len(source_rows),
        "status": "PASS",
    }


def main() -> int:
    try:
        result = validate()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
