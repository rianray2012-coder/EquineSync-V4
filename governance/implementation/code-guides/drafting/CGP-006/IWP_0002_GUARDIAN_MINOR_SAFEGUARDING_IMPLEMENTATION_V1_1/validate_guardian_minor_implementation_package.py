#!/usr/bin/env python3
"""Validate the CGP-006 IWP-0002 Guardian/Minor implementation evidence."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]

CONTROLLED_FILES = {
    "PROPOSED_FOUNDER_IMPLEMENTATION_AUTHORIZATION_AND_SCOPE_DISPOSITION_CGP006_IWP_0002_V1_1_0_2026-07-30.md": (
        "ab7f9332da372afd4259749745d0ce1b1442cd9ee4b448e39ee95300db6b74a8",
        6719,
    ),
    "CGP_006_IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_DIRECTIVE_V1_1_0.md": (
        "997a0e82afa51b415853b866e811dced7f61cbeece53e752d81858eb30a2c845",
        11287,
    ),
    "GUARDIAN_MINOR_SAFEGUARDING_PATCH_CONTRACT_V1_1_0.md": (
        "a2748a22b08e8de192c061c85967d3cef5162c249a7e27d70933e497c1f45ea9",
        5289,
    ),
    "GUARDIAN_MINOR_SECURITY_INVARIANT_AND_WORKFLOW_SPECIFICATION_V1_1_0.md": (
        "48db582df8e9177e233073f4de3a9b8d868e100ea0a0b487d64ff1d430e39bd5",
        6152,
    ),
    "GUARDIAN_RELATIONSHIP_AUTHORITY_CONSENT_AND_LIFECYCLE_DECISION_RECORD_V1_1_0.md": (
        "99ec8fbbaff8722bd199deb07554c3a873b4429ef484db2ad287e57cbc21aaf6",
        3720,
    ),
    "GUARDIAN_MINOR_WORKFLOW_ENFORCEMENT_MATRIX_V1_1_0.csv": (
        "c4b2b19ddebb44f84f78409b80844802ef38b0f2a5503903bb430ff9b2a6672c",
        6430,
    ),
    "GUARDIAN_MINOR_REGRESSION_AND_ABUSE_CASE_TEST_MATRIX_V1_1_0.csv": (
        "e40d94ff1e41c7f95ed978a8e9bf200626f11d67a59f9b0a8e5956296f93182b",
        8142,
    ),
    "GUARDIAN_MINOR_ROLLBACK_SUSPENSION_AND_EVIDENCE_PLAN_V1_1_0.md": (
        "44d74ee6dd036d404c632bb60259c2218e4716764118b3a1e848cee1f8b8841f",
        3101,
    ),
}

REQUIRED_PACKAGE_FILES = {
    "AFFECTED_PATH_AND_AUTHORITY_DRIFT_REVALIDATION.md",
    "AUDIT_PRIVACY_AND_REDACTION_EVIDENCE.md",
    "AUTHORIZED_IMPLEMENTATION_PATHS.csv",
    "AUTHORIZED_PATH_REPORT.md",
    "CHANGE_AWARE_BYPASS_REVIEW.md",
    "CONCURRENCY_ATOMICITY_AND_CACHE_REVALIDATION_EVIDENCE.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "EXTERNAL_ERROR_AND_INTERNAL_AUDIT_CODE_MAP.csv",
    "FINDING_AND_GAP_TREATMENT_RECORD.md",
    "FOUNDER_AUTHORIZATION_SOURCE_REGISTER.md",
    "FOUNDER_DIRECTIVE_CGP_006_IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_REAPPROVAL_IMPLEMENTATION_MERGE_CUSTODY_AND_CONDITIONAL_CLOSURE_V1_0_0.md",
    "FOUNDER_EXACT_BYTE_REAPPROVAL_AND_DIRECTIVE_RECORD.md",
    "FOUNDER_REAPPROVAL_RECORD_CGP006_IWP_0002_V1_1_0_2026-07-30.md",
    "GUARDED_WORKFLOW_ROUTE_AND_SYMBOL_INVENTORY.csv",
    "IMPLEMENTATION_CHANGE_RECORD.md",
    "LEGITIMATE_BEHAVIOR_PRESERVATION_REPORT.md",
    "ORIGINAL_PACKAGE_SOURCE_IDENTITY_AND_SUPERSESSION_RECORD_V1_0_0.json",
    "PACKAGE_MANIFEST.json",
    "PATCH_CONTRACT_EXECUTION_RECORD.md",
    "PER_MINOR_COMMUNICATION_COVERAGE_EVIDENCE.md",
    "PRE_FIX_REPRODUCTION_AND_REGRESSION_EVIDENCE.md",
    "REGRESSION_AND_ABUSE_TEST_RESULTS.csv",
    "RELATIONSHIP_AUTHORITY_AND_CONSENT_DATA_MODEL_RECORD.md",
    "REVIEW_FINDINGS_AND_DISPOSITION_MATRIX_V1_0_0.csv",
    "REVIEW_FINDINGS_AND_DISPOSITION_RECORD.csv",
    "ROLLBACK_AND_SUSPENSION_RECORD.md",
    "SCHEMA_AND_INDEX_CHANGE_RECORD.md",
    "SOURCE_FREEZE_AND_BASELINE_RECORD.json",
    "VALIDATION_REPORT.md",
    "WORKFLOW_ENFORCEMENT_COMPLETION_MATRIX.csv",
    "validate_guardian_minor_implementation_package.py",
    "test_validate_guardian_minor_implementation_package.py",
}

EXPECTED_WORKFLOWS = {
    "lesson_ready_and_lesson_participation",
    "messaging",
    "waiver",
    "document_signature",
    "media_release",
    "payment",
    "event_signup",
    "guardian_lifecycle_and_participant_removal",
}

IMPLEMENTED_PATHS = {
    "backend/core/minor_safety.py",
    "backend/core/minor_communication.py",
    "backend/core/lifespan.py",
    "backend/routes/student_guardians.py",
    "backend/routes/operations.py",
    "backend/routes/document_signatures.py",
    "backend/routes/billing.py",
    "backend/routes/recurring_charges.py",
    "backend/routes/care.py",
    "backend/tests/test_cgp006_iwp0002_guardian_minor_safeguarding.py",
}


def digest(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_text(path: Path, snippets: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            fail(f"{path.name} missing snippet: {snippet}")
    return text


def validate_controlled_files() -> None:
    for name, (expected_sha, expected_size) in CONTROLLED_FILES.items():
        path = ROOT / name
        if not path.is_file():
            fail(f"missing controlled file {name}")
        sha, size = digest(path)
        if sha != expected_sha or size != expected_size:
            fail(f"controlled file changed: {name}")


def validate_package_files() -> None:
    found = {path.name for path in ROOT.iterdir() if path.is_file()}
    missing = REQUIRED_PACKAGE_FILES - found
    if missing:
        fail(f"missing package evidence files: {sorted(missing)}")
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != "CGP006-IWP0002-GUARDIAN-MINOR-SAFEGUARDING-IMPLEMENTATION-V1.1":
        fail("unexpected package_id")
    if manifest.get("status") not in {
        "IMPLEMENTATION_EVIDENCE_COMPLETE_PENDING_PROTECTED_PR_MERGE",
        "POST_MERGE_CUSTODY_COMPLETE_CONDITIONAL_CLOSURE_READY",
    }:
        fail("unexpected implementation package status")
    expected_manifested = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"})
    if sorted(manifest.get("files", {}).keys()) != expected_manifested:
        fail("manifest file list mismatch")
    for name, meta in manifest["files"].items():
        sha, size = digest(ROOT / name)
        if sha != meta.get("sha256") or size != meta.get("bytes"):
            fail(f"manifest digest mismatch: {name}")

    checksum_lines = [line for line in (ROOT / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if line.strip()]
    expected_checksum_names = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "CHECKSUM_MANIFEST.sha256")
    actual_checksum_names = []
    for line in checksum_lines:
        try:
            sha, name = line.split("  ", 1)
        except ValueError:
            fail(f"bad checksum line: {line}")
        actual_checksum_names.append(name)
        actual_sha, _ = digest(ROOT / name)
        if sha != actual_sha:
            fail(f"checksum digest mismatch: {name}")
    if sorted(actual_checksum_names) != expected_checksum_names:
        fail("checksum file list mismatch")


def validate_source_identity() -> None:
    record = json.loads((ROOT / "SOURCE_FREEZE_AND_BASELINE_RECORD.json").read_text(encoding="utf-8"))
    if record.get("implementation_baseline_sha") != "9996e948ede39a968b8facd8afe15c2b1a345204":
        fail("baseline head mismatch")
    if record.get("source_zip", {}).get("sha256") != "6272108b389af3966f19dd14ab28a7f529ea31111cb8e1179e2ea86a51ce27ca":
        fail("source zip sha mismatch")
    if record.get("founder_directive", {}).get("sha256") != "2158eb46806e354b67fce284e6aadf32edd3739d39aa58ec68ac06d1172c1c6a":
        fail("founder directive sha mismatch")
    require_text(
        ROOT / "FOUNDER_EXACT_BYTE_REAPPROVAL_AND_DIRECTIVE_RECORD.md",
        [
            "EXACT_BYTE_PACKAGE_REAPPROVAL_AUTHENTICATED",
            "6272108b389af3966f19dd14ab28a7f529ea31111cb8e1179e2ea86a51ce27ca",
            "2158eb46806e354b67fce284e6aadf32edd3739d39aa58ec68ac06d1172c1c6a",
        ],
    )


def validate_authorized_paths() -> None:
    rows = read_csv(ROOT / "AUTHORIZED_IMPLEMENTATION_PATHS.csv")
    paths = {row["path"] for row in rows}
    missing = IMPLEMENTED_PATHS - paths
    if missing:
        fail(f"implemented path not authorized: {sorted(missing)}")
    if not any(path.endswith("/**") for path in paths):
        fail("package evidence path wildcard missing")
    report = (ROOT / "AUTHORIZED_PATH_REPORT.md").read_text(encoding="utf-8")
    if "PASS" not in report or "No unauthorized paths" not in report:
        fail("authorized path report is not passing")


def validate_workflow_and_results_records() -> None:
    completion_rows = read_csv(ROOT / "WORKFLOW_ENFORCEMENT_COMPLETION_MATRIX.csv")
    workflows = {row["workflow"] for row in completion_rows}
    if workflows != EXPECTED_WORKFLOWS:
        fail(f"workflow completion mismatch: {sorted(workflows)}")
    if any(row.get("status") != "IMPLEMENTED_AND_TESTED" for row in completion_rows):
        fail("workflow completion matrix has non-passing rows")

    results = read_csv(ROOT / "REGRESSION_AND_ABUSE_TEST_RESULTS.csv")
    if len(results) != 43:
        fail(f"expected 43 regression results, got {len(results)}")
    ids = [row["test_id"] for row in results]
    if ids != [f"GMS-T-{idx:03d}" for idx in range(1, 44)]:
        fail("regression result IDs are incomplete or out of order")
    if any(row["status"] != "PASS" for row in results):
        fail("regression result has non-pass status")


def validate_implementation_symbols() -> None:
    checks = {
        "backend/core/minor_safety.py": [
            "def guardian_minor_workflow_gate(",
            "GUARDIAN_WORKFLOW_CONSENT_COLLECTION",
            "def ensure_guardian_minor_safeguarding_indexes(",
            "def guardian_minor_public_error_detail(",
        ],
        "backend/core/minor_communication.py": [
            "async def message_guardian_minor_safeguarding_gate(",
            "require_guardian_participant=True",
        ],
        "backend/routes/student_guardians.py": [
            "guardian-consents",
            "authority_scopes",
            "revoke",
            "_guard_student_workflow",
        ],
        "backend/routes/operations.py": [
            "_enforce_guarded_students",
            "message_guardian_minor_safeguarding_gate",
            "service_request.event_signup.create",
        ],
        "backend/routes/document_signatures.py": [
            "_enforce_document_guard",
            "document_request.sandbox_envelope",
            "WORKFLOW_MEDIA_RELEASE",
        ],
        "backend/routes/billing.py": [
            "_enforce_payment_guard",
            "invoice.create",
            "invoice.pay",
        ],
        "backend/routes/recurring_charges.py": [
            "_payment_gate",
            "recurring_charge.create",
            "recurring_charge.update",
            "recurring_charge.materialize",
        ],
        "backend/core/lifespan.py": [
            "ensure_guardian_minor_safeguarding_indexes",
        ],
    }
    for rel, snippets in checks.items():
        require_text(REPO / rel, snippets)

    test_text = (REPO / "backend/tests/test_cgp006_iwp0002_guardian_minor_safeguarding.py").read_text(encoding="utf-8")
    found_ids = re.findall(r"def test_gms_t_(\d{3})_", test_text)
    if found_ids != [f"{idx:03d}" for idx in range(1, 44)]:
        fail("focused test file does not contain exactly GMS-T-001 through GMS-T-043")


def validate_boundaries() -> None:
    changed_text = "\n".join((REPO / rel).read_text(encoding="utf-8") for rel in IMPLEMENTED_PATHS if (REPO / rel).suffix == ".py")
    forbidden_provider_calls = [
        "stripe.",
        "docusign.",
        "requests.post(\"https://",
        "requests.post('https://",
        "wrangler deploy",
        "vercel deploy",
        "netlify deploy",
        "render deploy",
    ]
    for forbidden in forbidden_provider_calls:
        if forbidden in changed_text.lower():
            fail(f"forbidden provider/deployment marker in implementation source: {forbidden}")
    require_text(ROOT / "DIRECTIVE_EXECUTION_RECORD.md", ["No deployment", "No provider calls", "No GAP_0004"])
    require_text(ROOT / "FINDING_AND_GAP_TREATMENT_RECORD.md", ["scope-limited", "Pending protected merge"])


def main() -> int:
    validate_controlled_files()
    validate_package_files()
    validate_source_identity()
    validate_authorized_paths()
    validate_workflow_and_results_records()
    validate_implementation_symbols()
    validate_boundaries()
    print("PASS guardian/minor implementation package: 8 workflows, 43 tests, controlled files unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
